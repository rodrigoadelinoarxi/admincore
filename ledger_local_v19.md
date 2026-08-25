# Ledger de Migração Local — v19 (admincore-arxi)

Registo das correções feitas ao restaurar o dump do servidor externo no ambiente local.

- **BD:** `admincore_19_1`
- **Dump:** `admincore_19_20260824_101022.dump` (pg_dump -Fc, origem PG 16.14, BD `admincore`)
- **Config:** `custom/config/admincore-arxi.conf` (porta **8017**)
- **URL:** http://localhost:8017
- **Login:** `administradorARXI` / `demo1234` (uid 2)
- **Data:** 2026-08-24

> **Nota sobre a porta:** 8017 é a mesma porta usada por *todos* os configs do `odoo18`.
> Com este servidor a correr não é possível arrancar nenhum servidor v18 em simultâneo.

## Resumo

| # | Assunto | Estado |
|---|---|---|
| 1 | `load_menus` 422/500 — `user_menu_visibility` | **RESOLVIDO** |
| 2 | Erros OWL — `admin_expiration_panel` | **RESOLVIDO** |
| 3 | ~107.000 anexos de negócio sem ficheiro | por resolver (precisa filestore de origem) |
| 4 | Extensão `pgvector` em falta | sem impacto |
| 5 | `theme_*` + `studio_customization` sem código | por resolver (não estão em nenhum repo) |
| 6 | Comparação com master v17 | OK (31/31 módulos) |
| 7 | `Missing model` x118 (resíduos em `ir_model`) | por resolver, cosmético |
| 8 | `_gc_user_apikeys()` falha no autovacuum | **RESOLVIDO** |
| 9 | `casperventures` não instalava (12 vistas/relatórios) | **RESOLVIDO** |
| 10 | `product_uom` -> `product_uom_id` em `l10n_pt_sale` | **RESOLVIDO** (upstream, pelo colega) |
| 11 | 16 módulos não carregavam (`l10n_pt*`, `casperventures`) | **RESOLVIDO** |
| 12 | `view_mode` com `tree` em 132 ações (resíduo v17) | **RESOLVIDO** |
| 13 | Contas sem empresa: `account_account_res_company_rel` vazia | **BLOQUEANTE — precisa da BD v17** |
| 15 | `res.groups.category_id` removido (`base_internal_portal`) | **RESOLVIDO** |
| 16 | Vistas SQL desatualizadas (3 relatórios) | **RESOLVIDO** |
| 17 | `_select()` devolve `SQL`, não string (`casperventures`) | **RESOLVIDO** |
| 18 | `tz='Portugal'` inválido em PostgreSQL (257 registos) | **RESOLVIDO** |
| 19 | `budget_line` sem colunas `x_plan*_id` | **RESOLVIDO** |
| 20 | Ciclo financeiro parado (faturar/pagar/NC) | **BLOQUEADO pela secção 13** |
| 22 | Teste Playwright: 293 ecrãs, 0 regressões | **CONCLUÍDO** |

---

## 1. Webclient não arranca: `load_menus` 422/500 (`user_menu_visibility`) — RESOLVIDO

### Sintoma
Consola do browser em `/odoo`:

```
XHR GET /web/webclient/load_menus  [HTTP/1.1 422 UNPROCESSABLE ENTITY]
Uncaught (in promise) SyntaxError: JSON.parse: unexpected character at line 1 column 1
Missing (extension) parent templates: web_enterprise.DatabaseExpirationPanel
```

### Causa raiz — 2 incompatibilidades v17 -> v19 em `user_menu_visibility`

O endpoint `/web/webclient/load_menus` rebentava no servidor e devolvia uma página de
erro **HTML**. O JS fazia `JSON.parse()` desse HTML e falhava no `<` inicial — daí o
`unexpected character at line 1 column 1`. Sem menus, o webclient não arranca e o
`DatabaseExpirationPanel` nunca chega a ser registado (era **sintoma, não causa**).

Ambos os problemas estão em
`user_menu_visibility/models/ir_ui_menu.py`, que faz override de `load_menus`.

#### 1a. `create_action()` no report do Planning (HTTP 422)

```
File ".../user_menu_visibility/models/ir_ui_menu.py", line 44, in load_menus
    ir_act_report1.sudo().create_action()
File ".../enterprise/addons/planning/models/ir_actions_report.py", line 17, in create_action
    raise UserError("The Planning report cannot be added to the print menu. ...")
```

O módulo chama `create_action()` em **todos** os reports não atribuídos ao utilizador.
A v19 introduziu em `planning/models/ir_actions_report.py` um guard que **rejeita**
`planning.slot_report` no menu de impressão. Como a chamada era em bloco, bastava esse
report para rebentar o `load_menus` inteiro.

**Correção** — iterar report a report e ignorar os que recusam binding:

```python
from odoo.exceptions import UserError
...
for report in ir_act_report1.sudo():
    try:
        report.create_action()
    except UserError:
        continue
```

#### 1b. `groups_id` renomeado para `group_ids` (HTTP 500)

Depois da correção acima, passou a dar 500:

```
File ".../user_menu_visibility/models/ir_ui_menu.py", line 19
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
AttributeError: 'res.users' object has no attribute 'groups_id'
```

Na v19 o campo `res.users.groups_id` passou a chamar-se **`group_ids`**
(`odoo/addons/base/models/res_users.py:257`).

**Correção:**
```python
@tools.ormcache('frozenset(self.env.user.group_ids.ids)', 'debug')
```

Corrigida também a mesma ocorrência em
`internal_portal/internal_portal_attendances/models/res_users.py`
(`user.write({'groups_id': ...})` -> `'group_ids'`), que é uma escrita real.

### Verificação
```
login RPC                -> uid 2
/web/webclient/load_menus -> HTTP 200, 182.370 bytes, JSON válido, 37 apps
/odoo                     -> HTTP 200
web.assets_web.min.js     -> 9.195.960 bytes, JS válido
0 ERROR no log
```

### Nota — limpeza de assets (feita antes, NÃO era a causa)
Também foram apagados 273 attachments de assets, porque o dump veio **sem filestore**
(107.279 registos em `ir_attachment` para apenas 22 ficheiros em disco) e os bundles
apontavam para ficheiros inexistentes. É uma limpeza legítima e os assets regeneram-se,
mas **não era a causa do erro de JS** — o erro persistiu até corrigir o
`user_menu_visibility`. Se voltar a haver assets corrompidos:

```sql
DELETE FROM ir_attachment WHERE res_model='ir.ui.view' AND name LIKE '%assets%';
```

---

## 2. Erros de OWL no `admin_expiration_panel` — RESOLVIDO

Depois de resolver a secção 1 (menus a carregar outra vez), sobravam ainda estes erros
na consola do browser:

```
Missing (extension) parent templates: web_enterprise.DatabaseExpirationPanel
OwlError: An error occured in the owl lifecycle
Caused by: Error: Service user is not available
    useService@.../web.assets_web.min.js:4759
```

Módulo: `admin_expiration_panel` (mostra o painel de expiração só a admins).
**Duas** incompatibilidades v17 -> v19, ambas em `static/src/js/`.

### 2a. Serviço `user` removido na v19

```js
// ANTES (v17) — rebenta com "Service user is not available"
import { useService } from "@web/core/utils/hooks";
this.user = useService("user");
this.state.displayAlert = await this.user.hasGroup("base.group_erp_manager");
```

Na v19 **já não existe** um serviço `user` registado
(nenhum `registry.category("services").add("user", ...)` no core).
Passou a ser um import direto de `@web/core/user`, com `hasGroup()` no objeto.

```js
// DEPOIS (v19)
import { user } from "@web/core/user";
this.state.displayAlert = await user.hasGroup("base.group_erp_manager");
```

### 2b. Nome do template pai errado

```xml
<!-- ANTES — "Missing parent templates" -->
<t t-name="DatabaseExpirationPanel" owl="1"
   t-inherit="web_enterprise.DatabaseExpirationPanel" t-inherit-mode="extension">
```

Dois problemas:
1. `web_enterprise.DatabaseExpirationPanel` **não existe**. O template no core enterprise
   (`web_enterprise/static/src/webclient/home_menu/expiration_panel.xml:4`) chama-se
   apenas `DatabaseExpirationPanel`, sem prefixo de módulo.
2. Na v19 o template que herda tem de ter **nome próprio prefixado** com o módulo;
   não pode reutilizar o nome do pai.
3. O atributo `owl="1"` é obsoleto.

```xml
<!-- DEPOIS (v19) -->
<t t-name="admin_expiration_panel.DatabaseExpirationPanel"
   t-inherit="DatabaseExpirationPanel" t-inherit-mode="extension">
```

### 2c. Assets estavam comentados no manifest

Os dois ficheiros tinham sido comentados em `__manifest__.py` (tentativa de despistar o erro),
o que desativava o módulo por completo. Reativados:

```python
'assets': {
    'web.assets_backend': [
        'admin_expiration_panel/static/src/js/*.js',
        'admin_expiration_panel/static/src/js/*.xml',
    ],
},
```

Seguido de `-u admin_expiration_panel` para o manifest ser relido.

### Verificação
```
load_menus -> HTTP 200, 37 apps
bundle web.assets_web.min.js:
  registerTemplateExtension("DatabaseExpirationPanel", ...)   <- pai correto
  admin_expiration_panel.DatabaseExpirationPanel   PRESENTE
  web_enterprise.DatabaseExpirationPanel (nome errado)  AUSENTE
  displayAlert PRESENTE  -> módulo ativo, não neutralizado
```

---


## 3. Anexos de negócio em falta — POR RESOLVER (limitação do dump)

O `DELETE` acima só cobriu assets. Continuam ~107.000 attachments de negócio a apontar para
ficheiros que não existem localmente. **Não são regeneráveis** — só vêm do filestore de origem.

| Modelo | Anexos sem ficheiro |
|---|---|
| `account.move` | 43.728 |
| `documents.document` | 25.898 |
| `hr.payslip` | 8.438 |
| `hr.expense` | 4.941 |
| `discuss.channel` | 3.922 |
| `res.partner` | 2.296 |
| `mail.message` | 2.233 |
| `sale.order` | 2.188 |
| `account.batch.payment` | 2.042 |
| `sign.request` | 1.528 |
| `hr.employee` | 1.295 |

**Impacto:** abrir/descarregar qualquer destes anexos dá erro. Sem efeito no arranque nem na
navegação normal. Para resolver é preciso o filestore do servidor de origem (dump `with_fs`).

---

## 4. Extensão `pgvector` em falta — SEM IMPACTO

`pg_restore` deu 2 erros:
```
ERROR: extension "vector" is not available
```
Verificado que **não há nenhuma coluna do tipo `vector`** na BD
(`SELECT count(*) FROM information_schema.columns WHERE udt_name='vector'` -> 0).
Sem impacto. Se um dia for preciso: `apt install postgresql-16-pgvector`.

---

## 5. Módulos instalados na BD sem código em disco — POR RESOLVER

```
ERROR odoo.modules.loading: Some modules are not loaded, some dependencies or
manifest may be missing: ['theme_avantgarde', 'theme_cobalt', 'theme_common']
```

| Módulo | Estado BD | Registos | Notas |
|---|---|---|---|
| `theme_common` | installed | 3 | dependência dos temas |
| `theme_avantgarde` | installed | 153 | |
| `theme_cobalt` | installed | 149 | usado pelos sites **Brainr** (id 12) e **Gal Ventures** (id 20) |
| `studio_customization` | installed | 38 | ignorado em silêncio: 21 vistas, 8 campos custom, 9 regras de aprovação |

**Confirmado que estes módulos não existem em `odoo17/`, `odoo18/` nem `odoo19/`** — ou seja,
também não estão no código master v17 (`server-casperventures`). Não é perda da migração:
- os `theme_*` são temas de design Enterprise, vêm do repo de themes (não deste repo);
- o `studio_customization` é gerado pelo Odoo Studio no servidor de origem.

**Impacto:** só afeta os 2 websites acima e as customizações Studio. O backend arranca e
funciona normalmente.

---

## 6. Comparação com o código oficial v17 — OK

`odoo17/custom/addons/server-casperventures` vs `odoo19/custom/addons/admincore-arxi`,
**excluindo `arxi_certification`**:

- **31 módulos de cada lado, correspondência 1:1** — nenhum perdido, nenhum a mais.
- Versões dos manifests bumpadas para `19.0.*` — **exceto `deferrals_option`**,
  que ficou em `17.0.0.0.12` e por isso nem era instalável (corrigido; ver secção 11c).
- XML limpo: zero `<tree>`, zero `attrs=`/`states=`, `view_mode` já em `list`.
- Migração real feita em 11 módulos (`<tree>`→`<list>`, `@api.returns` removido,
  `ormcache_context`→`ormcache`).

### Padrões antigos que sobreviveram (v19 ainda tolera, mas avisa)

```
WARNING odoo.registry: Model attribute '_sql_constraints' is no longer supported,
please define models.Constraint on the model.
```

| Módulo | Padrão | Estado BD | Ação |
|---|---|---|---|
| `user_menu_visibility` | `groups_id` + `create_action()` | **installed** | **CORRIGIDO** (ver secções 1 e 2) |
| `internal_portal_attendances` | `groups_id` | **installed** | **CORRIGIDO** (ver secções 1 e 2) |
| `hr_attendance_reason` | `_sql_constraints` | **installed** | só aviso, funciona |
| `sh_purchase_dynamic_approval` | `_sql_constraints` + `groups_id` (4x) | uninstalled | por corrigir se for instalado |
| `product_multi_company` | `groups_id` (só em `tests/`) | installed | sem impacto em runtime |
| `hr_attendance_autoclose` | `groups_id` (só em `tests/`) | installed | sem impacto em runtime |
| `mail_smtp_imap_by_company` | `_sql_constraints` + `name_get()` | uninstalled | por corrigir se for instalado |

**Lição:** a comparação de ficheiros v17 vs v19 dava "OK" para o `user_menu_visibility`
(o ficheiro tinha sido tocado), mas a migração estava **incompleta** — o `ormcache_context`
foi convertido para `ormcache` sem trocar `groups_id` por `group_ids`. Ficheiro alterado
não significa ficheiro migrado.

Outros avisos (não bloqueantes): `@route(type='json')` deprecado a favor de `'jsonrpc'`
em `payment_eupago_cc`, `payment_eupago_mbway`, `arxi_quality_saft_api_client`.

Nota: dentro de `arxi_certification` faltam 40 módulos face à v17, mas **todos estão
`uninstalled` na BD** — a poda foi intencional.

---

## 7. `Missing model` x118 no arranque — COSMÉTICO, por resolver

```
ERROR odoo.addons.base.models.ir_model: Missing model irs.tax.table
ERROR odoo.addons.base.models.ir_model: Missing model unique.report
ERROR odoo.addons.base.models.ir_model: Missing model account.transfer.model
... (118 no total)
```

Resíduos em `ir_model` referentes aos 40 módulos de `arxi_certification` que estão
`uninstalled` e sem código carregado (ver secção 6). **Já apareciam antes de qualquer
alteração feita aqui** — não foram introduzidos pelas correções.

Sem impacto funcional: são registos órfãos de metadados. Limpam-se com um
`--update=all` depois de decidir que módulos ficam mesmo instalados, ou manualmente
via `DELETE FROM ir_model WHERE model IN (...)` — mas convém confirmar antes que
nenhum registo de negócio lhes aponta.

---

## 8. `_gc_user_apikeys()` falha no autovacuum — RESOLVIDO

```
ERROR odoo.sql_db: bad query: DELETE FROM "auth_totp_device"
    WHERE expiration_date IS NOT NULL AND expiration_date < now() at time zone 'utc'
ERROR odoo.addons.base.models.ir_autovacuum: Failed auth_totp.device()._gc_user_apikeys()
ERROR odoo.sql_db: bad query: DELETE FROM "res_users_apikeys" ...
ERROR odoo.addons.base.models.ir_autovacuum: Failed res.users.apikeys()._gc_user_apikeys()
```

A coluna `expiration_date` não existe em `auth_totp_device` nem em `res_users_apikeys`.
Confirmado:

```sql
SELECT column_name FROM information_schema.columns
WHERE table_name IN ('auth_totp_device','res_users_apikeys');
-- id, name, user_id, scope, index, key, create_date   <- sem expiration_date
```

O campo existe no código v19 (`odoo/addons/base/models/res_users.py:1529`), mas estas
duas tabelas **não são geridas pelo ORM** — são criadas por SQL cru em `init()` com
`CREATE TABLE IF NOT EXISTS` (`res_users.py:1531-1544`).

**Consequência importante:** como as tabelas já existem (vieram do dump), o
`CREATE TABLE IF NOT EXISTS` não faz nada e a coluna **nunca é adicionada**, por mais
`-u base` / `--update=all` que se corra. Tem de ser manual:

```sql
ALTER TABLE res_users_apikeys ADD COLUMN IF NOT EXISTS expiration_date timestamp without time zone;
ALTER TABLE auth_totp_device  ADD COLUMN IF NOT EXISTS expiration_date timestamp without time zone;
```

Só afeta o garbage collector das API keys / dispositivos TOTP (corre no cron do
autovacuum). Não afeta login nem uso normal.

### Correção aplicada e verificação
As duas colunas foram adicionadas com o `ALTER TABLE` acima. Depois disso:

```
res.users.apikeys._gc_user_apikeys()  -> OK
auth_totp.device._gc_user_apikeys()   -> OK
load_menus                            -> HTTP 200, 37 apps (sem regressão)
```

---

## 9. `casperventures` não instalava — RESOLVIDO

### Sintoma
`RPC_ERROR` ao abrir Contabilidade:
```
ValueError: O elemento '<xpath expr="//a[@name='335']">' não foi encontrado na vista ascendente
```
E `-u casperventures` falhava com `Failed to load registry`. Cada correção destapava a
seguinte: **12 vistas/relatórios** partidos pela v19, todos em `casperventures/`.

> **Nenhum ficheiro de `arxi_certification/` foi alterado.** Só se ajustaram os *seletores*
> e nomes de campos do lado do `casperventures` para acompanharem a v19.

### Padrões de mudança encontrados na v19

| # | Padrão v17 | v19 | Onde |
|---|---|---|---|
| 1 | ação `account_followup.action_view_list_customer_statements` | deixou de existir; sobra registo órfão na BD | `views/account_journal_dashboard_views.xml` |
| 2 | `<div t-field="company.report_footer">` | `<span>` no `external_layout_boxed` | `reports/report_payment_receipt.xml` |
| 3 | `<strong>` no subtotal + `amount_by_group['tax_group_name']` | `<span>` + `tax_group['group_name']`; `account.tax_groups_totals` desapareceu | `reports/shared_tax_totals_brainr.xml` |
| 4 | `@class='text-end o_price_total'` | v19 acrescentou `text-nowrap` -> usar `hasclass()` | `reports/account_custom_report_brainr.xml` |
| 5 | `inalterable_hash`, `atcud` | **`pt_arxi_inalterable_hash`, `pt_arxi_atcud`** | 2 ficheiros, 31 ocorrências |
| 6 | hash/ATCUD em `web.external_layout_*` | injetados por `l10n_pt_certificate.external_layout_*` -> `inherit_id` repontado | `reports/account_custom_report_brainr.xml` |
| 7 | QR em `report_saleorder_document` (`atcud_qr_code`) | template autónomo `l10n_pt_sale.qr_code_container_sale_order` (`qr_code_container`) | `reports/sale_custom_report_brainr.xml` |
| 8 | `<h2><span t-field="doc.name">` | `<t t-set="layout_document_title">` | `reports/sale_custom_report_brainr.xml` |
| 9 | `//field[@name='order_line']/tree//` | `/list//` | `views/sale_views.xml` |
| 10 | `group[@name='active_group']` | `group[@name='user']` (2 instâncias) | `views/hr_employee_views.xml` |
| 11 | `parent::ul/following-sibling::div` | `following-sibling::div[1]` | `reports/account_custom_report_brainr.xml` |
| 12 | `optional="1"` em `<xpath>` | **não existe na v19**: é ignorado e o alvo em falta é fatal | vários |

### 4 templates desativados (originais em `casperventures/reports/_disabled_v19/`)

Dependiam de estrutura que **deixou de existir** no `report_invoice_document` da v19
(`qrcode_pt_top_with_shipping`, `qrcode_pt_top_without_shipping`, `address_block_anchor`,
spans de ATCUD/hash). Na v19 esse conteúdo passou para
`l10n_pt_certificate.qr_code_container_invoice` e para os `external_layout_*`.

| Template | O que fazia |
|---|---|
| `report_hash_footer_brainr` | escondia hash/ATCUD no rodapé |
| `report_invoice_remove_original_qr` | removia os QR originais do topo/fundo |
| `report_invoice_qrcode_fix` | reposicionava o QR depois do bloco de moradas |
| `remove_original_block_after_shipping` | removia o bloco ATCUD após shipping |

> **A VALIDAR:** estes 4 templates *escondiam* hash/ATCUD/QR nos relatórios custom.
> Com eles desativados, esses elementos **podem voltar a aparecer** nos documentos das
> empresas com `use_custom_report`. Precisa de confirmação visual e, se for para manter o
> comportamento antigo, de redesenho contra os novos templates.

### Nota — archs em cache na BD

Odoo valida as vistas **já existentes na BD** antes de aplicar o XML novo, por isso corrigir
só o ficheiro não chega: o upgrade continua a falhar com a mensagem antiga. Foi preciso, em
paralelo, atualizar/desativar os registos em `ir_ui_view` (7 archs com o campo antigo
renomeados via SQL, 6 vistas obsoletas postas a `active=false`).

### Verificação
```
-u casperventures            -> Registry loaded in 12.297s  (sem erros)
account.journal get_views    -> OK (list, kanban, form, search)   <- erro original resolvido
get_views OK em: account.move, sale.order, hr.employee, res.partner,
                 account.payment, account.asset, product.template
render payment receipt       -> OK, 6.944 bytes
```

---

## 10. `product_uom` -> `product_uom_id` em `l10n_pt_sale` — RESOLVIDO (upstream)

Ao renderizar um sale order:
```
QWebError: KeyError: 'product_uom'
Template: l10n_pt_sale.report_saleorder_document_mock (vista 4278)
Element: <span t-field="line.product_uom" groups="uom.group_uom"/>
```

Na v19 `sale.order.line.product_uom` passou a **`product_uom_id`**
(`odoo-server/addons/sale/models/sale_order_line.py:132`).

**Pré-existente, não introduzido pelas correções da secção 9** — `casperventures` não tem
nenhuma referência a `product_uom`. O template afetado está em
`arxi_certification/l10n_pt_sale/`, que por indicação do utilizador **não foi tocado**.

**Estado (2026-08-24, após novo código do colega):** já **corrigido upstream** — o
`l10n_pt_sale/report/sale_order_templates.xml` passou a usar `product_uom_id`.
Não foi preciso alterar nada do nosso lado.

### Nota — `wkhtmltopdf` em falta
`_render_qweb_pdf` falha com "Não é possível localizar Wkhtmltopdf neste sistema".
É limitação do ambiente local, não da migração. O render em HTML funciona.

---

## 11. 16 módulos não carregavam — RESOLVIDO

### Sintoma
Ao abrir as Definições:
```
OwlError: The following error occurred in onWillStart:
"res.config.settings"."partner_ref" field is undefined.
```

E no arranque:
```
ERROR odoo.modules.loading: Some modules are not loaded: ['ARXI_CERTIFICATION_PATCH',
'arxi_quality_saft_api_client', 'casperventures', 'l10n_pt_ao', 'l10n_pt_ao_access',
'l10n_pt_ao_journal_entry', 'l10n_pt_ao_saft', 'l10n_pt_ao_sale', 'l10n_pt_certificate',
'l10n_pt_delivery', 'l10n_pt_reports_arxi', 'l10n_pt_sale', 'l10n_pt_sale_stock',
'l10n_pt_stock', 'l10n_pt_website_payment', ...]
```

O `partner_ref` era **sintoma, não causa**: a vista `l10n_pt_ao.res_config_settings_view_form`
existia na BD, mas o módulo `l10n_pt_ao` não carregava, por isso o campo nunca era definido
em Python.

Havia **3 bloqueios independentes**, em cascata.

### 11a. `contract_instance_checker` fora do `addons_path`

O `l10n_pt_ao` declara `contract_instance_checker` nos `depends`, e o módulo não estava
em nenhum caminho carregado:

```
WARNING odoo.modules.module_graph: module l10n_pt_ao: some depends are not loaded
    (contract_instance_checker), skipped
```
Tudo o resto (`l10n_pt_*`, `casperventures`, ...) caía por dependência indireta.

**Resolução:** o módulo foi **movido para fora da certificação e passou para o bundle
`arxi-quality`** — de `arxi_certification/` para
`custom/addons/admincore-arxi/arxi-quality/contract_instance_checker`.
Esse caminho já constava do `addons_path`, pelo que não foi preciso alterar a config.

### 11b. `ir_model_fields.translate` com a string `'false'` (2315 campos)

Instalar o módulo rebentava com:
```
psycopg2.errors.CannotCoerce: cannot cast type integer to jsonb
LINE 1: ...TER COLUMN "company_id" TYPE jsonb USING "company_id"::jsonb
```
num **Many2one** (`contract.instance.status.company_id`), que nunca deveria ser jsonb.

**Causa raiz.** `ir_model_fields.translate` é `varchar`, e a v19 só reconhece
`NULL`, `standard`, `html_translate`, `xml_translate`. O dump trouxe **2315 campos com a
string `'false'`** e 16 com `'true'`. O core faz:

```python
# odoo/modules/loading.py:395
cr.execute("SELECT model || '.' || name, translate FROM ir_model_fields WHERE translate IS NOT NULL")
```

`'false'` **não é NULL**, por isso esses campos entram na lista de "traduzidos na BD".
Depois, em `odoo/orm/model_classes.py:386`:

```python
field_translate = FIELD_TRANSLATE.get(<valor>, True)   # 'false' não está no dict -> True
fields_.append(type(fields_[0])(translate=field_translate))
```

`FIELD_TRANSLATE` só tem `{None: False, 'standard': True, 'html_translate': ..., 'xml_translate': ...}`,
logo `.get('false', True)` devolve **`True`** e o campo é forçado a traduzível → coluna `jsonb`,
mesmo sendo Many2one.

**Correção:**
```sql
UPDATE ir_model_fields SET translate = NULL       WHERE translate = 'false';  -- 2315
UPDATE ir_model_fields SET translate = 'standard' WHERE translate = 'true';   -- 16
```
(os 16 `'true'` eram todos char/html genuinamente traduzíveis — verificados um a um)

### 11c. `deferrals_option` com manifest em `17.0`

```
WARNING odoo.modules.module_graph: module deferrals_option: not installable, skipped
```
As dependências existiam todas; o manifest é que ainda dizia `"version": "17.0.0.0.12"`.
Corrigido para `19.0.0.0.12`.

> **Correção a um levantamento anterior (secção 6):** ficou escrito que *todas* as versões
> estavam bumpadas para `19.0`. Estava errado — este manifest usa **aspas duplas** e escapou
> à verificação, que só apanhava aspas simples. Ao verificar com `ast.literal_eval` em vez de
> regex, apareceu como o único fora de `19.0`.

### Verificação
```
addons paths          -> sem caminhos temporários
Registry loaded       -> só faltam theme_avantgarde/cobalt/common (secção 5)
load_menus            -> 37 apps
Definições            -> 473 campos, partner_ref presente, 0 campos do arch em falta
get_views OK          -> account.journal, account.move, sale.order, res.company,
                         hr.employee, account.payment, stock.picking
```

---

## 12. `View types not defined tree found in act_window action` — RESOLVIDO

### Sintoma
```
UncaughtPromiseError
Uncaught Promise > View types not defined tree found in act_window action 667
    _executeActWindowAction@.../web.assets_web.min.js:10702:26
```
A ação 667 é a `sale.product_template_action` ("Products").

### Causa
Na v19 o tipo de vista `tree` foi renomeado para **`list`**. A ação tinha ficado com o
valor da v17:
```
view_mode = kanban,tree,form,activity
```
O webclient lê o `view_mode` diretamente e rejeita `tree`.

**Não era um problema pontual:** o varrimento à BD encontrou **132 ações** com `tree`,
mais **8** registos em `ir_act_window_view`. Praticamente todas de módulos **core/enterprise**
(`base` 27, `hr_payroll` 21, `account_consolidation` 12, `stock` 9, `documents` 7,
`account` 6, ...) — resíduo do dump v17 que o upgrade não converteu. Nada a ver com os
addons custom.

### Correção
```sql
BEGIN;
UPDATE ir_act_window
SET view_mode = regexp_replace(view_mode, '(^|,)tree(,|$)', '\1list\2', 'g')
WHERE view_mode LIKE '%tree%';          -- 132
UPDATE ir_act_window_view SET view_mode = 'list' WHERE view_mode = 'tree';   -- 8
COMMIT;
```

### Verificação
```
ir_act_window com 'tree'      -> 0
ir_act_window_view com 'tree' -> 0
ação 667                      -> kanban,list,form,activity
/web/action/load (8 ações)    -> 8 OK, 0 com erro
```

### O que ficou deliberadamente por corrigir

**63 archs de vistas ainda com `<tree>`** em `ir_ui_view`. Os donos estão **todos
`uninstalled`** (`hr_payroll` 20, `account_consolidation` 16, `documents` 9,
`l10n_pt_hr_payroll` 3, `l10n_pt_payroll_unique_report` 3, ...), pelo que nunca são
carregados e não causam erro. Se algum destes módulos vier a ser instalado, os archs
precisam de `<tree>` -> `<list>` primeiro.

### Falso positivo registado: `grid` é válido

Um varrimento a `view_mode` inválidos assinalou 7 ações de folhas de horas com `grid`
(ids 133, 625, 628, 696, 967, 1423, 1710). **`grid` é um tipo de vista legítimo na v19**,
adicionado pelo `web_grid` (instalado, 15 vistas do tipo):
```python
# enterprise/addons/web_grid/models/ir_actions.py:10
view_mode = fields.Selection(selection_add=[('grid', "Grid")], ondelete={'grid': 'cascade'})
```
Não foram alteradas. Fica o registo para não serem "corrigidas" por engano no futuro.

---

## 13. Contas sem empresa (`account_account_res_company_rel` vazia) — BLOQUEANTE

### Sintoma
```
UserError: Uh-oh! You've got some company inconsistencies here:
- "account.tax.repartition.line,36102" belongs to company "Admincore, Unipessoal Lda"
  while "Account" (account_id: 'IVA - Dedutível - Outros bens e serviços')
  belongs to another company.
```
E, silenciosamente: `account.account` devolve **0 registos** a qualquer utilizador.

### Causa raiz
Na v19 o `account.account.company_id` (many2one) foi substituído por **`company_ids`**
(many2many, tabela `account_account_res_company_rel`). Nesta BD:

```sql
SELECT count(*) FROM account_account;                    -- 15451
SELECT count(*) FROM account_account_res_company_rel;    --     0   <-- vazia
-- e a coluna antiga já não existe:
SELECT column_name FROM information_schema.columns
 WHERE table_name='account_account' AND column_name LIKE '%compan%';   -- 0 linhas
```

**As 15.451 contas do plano não estão associadas a nenhuma empresa.**

**Confirmado que vem da origem, não do restore local** — inspeção direta ao ficheiro `.dump`:
```bash
pg_restore -t account_account_res_company_rel -a -f - <dump> | grep -c '^[0-9]'   # 0
```
A tabela já vinha vazia. Um novo dump da mesma origem não resolve.

Só o `account.account` foi afetado: `account_journal` e `account_tax` mantêm `company_id`.

### Confirmação visual na interface (2026-08-24)

Ao abrir uma fatura (`Faturação > Clientes > Faturas`, doc `FT 2026/0012`), o utilizador
recebe o diálogo **"Erro de Acesso"**:

```
"Parece que se deparou com alguns registos secretos."
"Desculpe, Administrator (id=2) não tem acesso a 'leitura':"
 - Conta, Serviços principais PT (account.account: 3562)

"A responsabilidade é das seguintes regras:"
 - Account multi-company
```

A regra citada é exactamente a `account.account_comp_rule` da secção 12. Verificado:

```sql
SELECT a.id, a.code,
       (SELECT count(*) FROM account_account_res_company_rel r
         WHERE r.account_account_id = a.id) AS n_empresas
FROM account_account a WHERE a.id = 3562;
--  3562 | 7211 | 0      <-- zero empresas associadas
```

**Não é um problema de permissões do utilizador** (o uid 2 é administrador e
`check_access` passa) — a conta simplesmente não pertence a nenhuma empresa, por isso a
regra multi-company esconde-a de todos.

### O que isto explica
- **abrir uma fatura existente dá "Erro de Acesso"** (confirmado na UI)
- `account.account` -> 0 registos (a regra multi-company filtra tudo)
- a regra 62, mesmo corrigida para `company_ids` (secção 12), continua a devolver zero
- **7 módulos não atualizam** (ver abaixo)

### Por que não foi reconstruído

Fontes possíveis para inferir a empresa de cada conta:

| Fonte | Contas cobertas |
|---|---|
| xmlid `account.<company_id>_chart_...` | 3.241 |
| `account_move_line` | 1.932 |
| `account_tax_repartition_line` + defaults de journals | ~370 |
| **sem qualquer origem** | **10.619** |

Tentou-se ainda inferir por proximidade de `id` (os planos foram criados em blocos
sequenciais por empresa; o padrão é bom — **492 códigos repetem-se exatamente 17×**,
coerente com plano individual por cada uma das 17 empresas `pt_arxi`). Mas o teste de
coerência reprovou:

```sql
-- atribuindo cada conta à empresa da conta conhecida mais próxima por id:
-- 85 empresas ficariam com o MESMO código de conta duplicado
```

Isso prova que a inferência mistura planos entre empresas. **Não foi aplicada**: são dados
fiscais e uma atribuição errada tem impacto legal.

### Resolução necessária (fora do alcance local)

O preenchimento de `company_ids` é feito pelo **serviço de upgrade da Odoo** (o
`odoo-server/odoo/upgrade` local está vazio) e falhou silenciosamente no upgrade da origem.

1. **BD v17 original** (pré-upgrade), onde `account_account.company_id` ainda existe —
   reconstrução trivial e 100% fiável; **é o caminho recomendado**; ou
2. repetir o upgrade com o serviço oficial, verificando no fim que
   `account_account_res_company_rel` **não** fica vazia.

### Módulos bloqueados por isto (7)
`l10n_pt_certificate`, `l10n_pt_reports_arxi`, `l10n_pt_ao`, `l10n_pt_ao_saft`,
`l10n_pt_ao_reports`, `l10n_pt_ao_access`, `account_asset_law`, `contract_instance_checker`.

Todos falham com o mesmo `UserError`. **Não são 7 problemas — é 1.**
O primeiro a tropeçar é o script `l10n_pt_reports_arxi/migrations/1.43/post-create_m35_taxes.py`,
que cria as taxas M35 por empresa: o script está correto (usa `with_company()` + `_load_data`),
falha apenas porque as contas não pertencem a empresa nenhuma.

---

## 14. Atualização para o código novo do colega (2026-08-24)

Entrou código novo por git (`5fa8061`, `60cfa41`): nova versão de `deferrals_option`,
`contract_instance_checker` e vários módulos de certificação.

> **Nota de método:** o `-u all` foi tentado e **rebentou num menuitem do `stock`** (core),
> sem relação com o que mudou. Passou-se a atualizar **módulo a módulo**, por ordem de
> dependência, para isolar falhas.

### Atualizados com sucesso (8)
```
product_sale_history     l10n_pt_ao_journal_entry
deferrals_option         l10n_pt_stock
l10n_pt_website_payment  l10n_pt_sale_stock
l10n_pt_delivery         l10n_pt_sale + casperventures
```

### Correções necessárias (3 ficheiros, todos fora de `arxi_certification`)

**14a. `product_sale_history/views/partner_views.xml`** — `<list editable="true">`

Resíduo da conversão `<tree>`->`<list>`: `editable="true"` era válido em `<tree>` na v17,
mas a v19 só aceita `top`/`bottom`.
```
The "editable" attribute of list views must be "top" or "bottom", received true
```
Corrigido para `editable="bottom"`.

**14b/14c. Relatórios do `casperventures` (fatura e venda)**

O código novo envolveu o conteúdo das linhas num `<div class="pt_arxi_line_clip">`, pelo
que o `<span>` deixou de ser filho direto do `<td>`:

```xml
<!-- antes -->  //td[@name='account_invoice_line_name']/span
<!-- v19   -->  //td[@name='account_invoice_line_name']//span[@t-esc='line.name']

<!-- antes -->  //td[@name='td_name']/span
<!-- v19   -->  //td[@name='td_name']//span[@t-esc='line.name']
```

Passou-se também de `t-field` + `t-options="{'widget':'text'}"` para **`t-esc`**,
acompanhando o pai. O comentário no template do colega explica porquê: o widget `text`
chama `nl2br()`, transformando newlines em `<br/>` literais em vez de deixar o browser
decidir a quebra por largura.

### Ainda por atualizar (7)
Bloqueados pela secção 13. Assim que as contas tiverem empresa, devem atualizar em cadeia.

### Verificação
```
Registry loaded    -> só faltam os 3 themes (secção 5)
load_menus         -> 37 apps
account.move       -> 113.824 registos     sale.order       -> 3.687
account.asset      ->   1.121 registos     res.partner      -> 5.187
product.template   ->     926 registos     stock.picking    ->   492
account.account    ->       0 registos     <-- bloqueio da secção 13
```

---

## 15. `res.groups.category_id` removido — RESOLVIDO

### Sintoma
```
Occured on model crm.team
ValueError: Invalid field res.groups.category_id in condition ('category_id', '=', 127)
  File ".../internal_portal/base_internal_portal/models/res_groups.py", line 45,
      in get_portal_groups_to_view
    groups = self.search([('category_id', '=', categ_id.id)])
```

O erro aparecia no `crm.team`, mas a origem é o `base_internal_portal`: faz override de
`fields_get` em `res.users`, por isso rebentava em **qualquer vista que carregasse
utilizadores** — o modelo no erro é acidental.

### Causa
Na v19 o `res.groups.category_id` **deixou de existir**. A categoria passou para um modelo
intermédio novo:

```
res.groups --privilege_id--> res.groups.privilege --category_id--> ir.module.category
```

### Três APIs removidas no mesmo ficheiro

Ficheiro: `internal_portal/base_internal_portal/models/res_groups.py`

| Linha | v17 | v19 |
|---|---|---|
| 24, 45 | `('category_id', ...)` | `('privilege_id.category_id', ...)` |
| 39 | `g.trans_implied_ids` | `g.all_implied_ids` |
| 25 | `super().get_application_groups(domain)` | **o método já nem existe no core v19** |

O terceiro era o mais traiçoeiro: não dava erro no arranque, só quando o método fosse
efetivamente chamado. Ficou defensivo — se o core não o tiver, faz `search()` direto:

```python
_super = getattr(super(GroupsView, self), 'get_application_groups', None)
if _super is None:
    return self.search(domain)
return _super(domain)
```

Corrigido também um efeito secundário no mesmo método: fazia `domain.append(...)`, mutando
a lista recebida do chamador. Passou a `domain = list(domain) + [...]`.

### Verificação
```
-u base_internal_portal  -> Registry loaded
get_views OK             -> crm.team, res.users, res.groups, crm.lead, sale.order
```

---

## 16. Vistas SQL desatualizadas — RESOLVIDO

Modelos de relatório (`_auto = False`) mantinham na BD o SQL da v17, sem colunas que a v19
adicionou:

```
UndefinedColumn: column event_sale_report.is_published does not exist
UndefinedColumn: column report_project_task_user.sale_line_id does not exist
UndefinedColumn: column helpdesk_ticket_report_analysis.remaining_hours_so does not exist
```

Resolvido com `-u event_sale,project,helpdesk`, que recria as vistas SQL. O `sign.request`
(`Expected singleton`) também deixou de falhar.

### Falso positivo: `board.board`
```
UndefinedTable: relation "board_board" does not exist
```
**Não é um bug.** O modelo tem `_auto = False` e **não tem tabela por design**
(`odoo/addons/board/models/board.py:10`). O erro veio do meu varrimento a fazer `search()`
num modelo virtual; a ação real usa vista `form` e nunca toca na tabela.
Confirmado: `board.board.get_views()` -> OK, o painel abre.

---

## 17. `_select()` devolve `SQL`, não string — RESOLVIDO

`casperventures/models/account_invoice_report.py` estendia a query do relatório de faturas
concatenando uma string:

```python
# v17
return super()._select() + ", move.partner_id AS partner_id_value"
# TypeError: unsupported operand type(s) for +: 'SQL' and 'str'
```

Na v19 `_select()` está anotado `-> SQL` e devolve um objeto `SQL`
(`addons/account/report/account_invoice_report.py:80`), que não suporta `+` com `str`.

```python
# v19
from odoo.tools import SQL
def _select(self) -> SQL:
    return SQL("%s, move.partner_id AS partner_id_value", super()._select())
```

Rebentava a **Análise de Faturas** (`Faturação/Relatórios/Gestão`).

---

## 18. `tz='Portugal'` inválido em PostgreSQL — RESOLVIDO

```
InvalidParameterValue: time zone "Portugal" not recognized
```
(em `project.timesheet.forecast.report.analysis`)

**A subtileza:** `Portugal` **é** um alias válido em Python/pytz, mas **não existe** em
`pg_timezone_names`. Por isso o ORM nunca se queixava — só rebentava em queries SQL que
fazem `AT TIME ZONE`, o que tornava o problema quase invisível.

| Tabela | Registos |
|---|---|
| `res_partner` | 158 |
| `resource_resource` | 76 |
| `resource_calendar` | 23 |

```sql
UPDATE res_partner       SET tz='Europe/Lisbon' WHERE tz='Portugal';
UPDATE resource_calendar SET tz='Europe/Lisbon' WHERE tz='Portugal';
UPDATE resource_resource SET tz='Europe/Lisbon' WHERE tz='Portugal';
```
`Europe/Lisbon` é equivalente e válido em pytz **e** em PostgreSQL. Zero inválidos restantes.

---

## 19. `budget_line` sem colunas `x_plan*_id` — RESOLVIDO

```
ValueError: Invalid field budget.line.x_plan7_id in condition ('x_plan7_id', 'in', ...)
```
(ao abrir `Faturação/Configuração/Contabilidade Analítica/Contas Analíticas`)

### Causa
**Não é um campo Studio órfão** (foi a primeira hipótese, errada). O Odoo **gera
automaticamente** uma coluna por cada plano analítico, com o nome `x_plan<id>_id`
(`analytic/models/analytic_plan.py:118`, `_strict_column_name()`).

Modelos que herdam `analytic.plan.fields.mixin`:
`account.analytic.line`, `budget.line`, `budget.report`, `project.project`.

Estado antes da correção:
- `account_analytic_line` -> ~400 colunas `x_plan*_id`
- `budget_line` -> **0 colunas**, apesar de herdar o mixin

O `_sync_all_plan_column()` não correu para o `budget.line` durante o upgrade.

### Correção
Usado o método **oficial** do Odoo (não SQL manual, para os `ir.model.fields` ficarem
coerentes com as colunas):

```python
env['account.analytic.plan'].sudo().search([])._sync_all_plan_column()
# 460 planos -> 413 colunas criadas em budget_line
```

Requer **restart do servidor** a seguir, para o registry carregar os campos novos.

> **Nota de método:** ao investigar procurou-se `analytic.plan.fields.mixin` em
> `odoo-server/addons/account_budget/` e concluiu-se (erradamente) que `budget.line` não
> herdava o mixin. O `account_budget` é **enterprise** — o ficheiro certo é
> `enterprise/addons/account_budget/models/budget_line.py:12`. Confirmar sempre em que
> repositório vive o módulo antes de concluir.

---

## 20. Ciclo financeiro bloqueado (faturar/pagar/nota de crédito) — consequência da secção 13

Teste de **fluxos de negócio reais** (criar/confirmar/faturar/pagar, em transação revertida):

### Resultado final (após corrigir os dados de teste)

| Fluxo | Resultado |
|---|---|
| **Compras**: encomenda **com linhas** -> confirmar | **OK** (61,50 EUR, estado `purchase`) |
| **Compras**: -> receber mercadoria | **OK** |
| **RH**: ausência -> aprovar | **OK** (estado `validate`) |
| **Email**: render do template de orçamento | **OK** (1164 chars) |
| **Email**: render do template de fatura | **OK** (928 chars) |
| **Email**: `message_post` ao cliente | **OK** (1 destinatário) |
| **Inventário**: validar transferência | sem transferências pendentes para testar |
| Vendas: orçamento -> confirmar | bloqueado: webservice ATCUD (**esperado**, ver abaixo) |
| Faturação: registar pagamento | **FALHA**: `company inconsistencies` |
| Faturação: nota de crédito | **FALHA**: `AccessError` |

### Alcance real do bloqueio da secção 13

O problema das contas sem empresa **não afeta apenas emitir faturas**: atinge também
**registar pagamentos** e **emitir notas de crédito**. O ciclo financeiro completo está
parado, não só a emissão.

### Fluxo real das Vendas: draft -> **Publicar** -> Confirmar

**Descoberto por inspeção do DOM no browser** (o Playwright não o revela: reporta apenas
"guardado, OK"). Num orçamento novo a barra de botões é:

```
Enviar | Imprimir | Pré-visualizar | Publicar        <-- NÃO há "Confirmar"
```

Causa, em `arxi_certification/l10n_pt_ao_sale/views/sale_order_views.xml`:
```xml
<!--Hide draft confirm button-->
<xpath expr="//button[@name='action_confirm'][2]" position="attributes">
    <attribute name="invisible">True</attribute>
<!-- e acrescenta: -->
<button name="action_quotation_sent" string="Post" invisible="state != 'draft'" class="btn-primary"/>
```
O `action_confirm` do core tem `invisible="state != 'sent'"`.

| Estado | Botão principal visível |
|---|---|
| `draft` | **Publicar** (`action_quotation_sent`) |
| `sent` | **Confirmar** (`action_confirm`) |
| `sale` | (nenhum) |

**É intencional**, não é bug: a certificação obriga a publicar (atribuir numeração/ATCUD)
antes de confirmar. Validado contra registos reais dos 3 estados.

> **Erro de método corrigido:** o primeiro teste de fluxos fazia `create()` ->
> `action_confirm()` directamente, saltando o `action_quotation_sent()`. Estava a testar um
> caminho que **na interface nem é possível**. Testar sempre pela ordem que a UI impõe.

### Falha ESPERADA: webservice da certificação

```
UserError: Comunicação com Webservice não é suportada no modo de Teste.
  at_webservice_mixin.at_ws_communication  (via get_atcud_for_sale -> account_series.action_activate)
```

Dispara no **Publicar** (não no Confirmar). **Não é um bug** — o módulo bloqueia a
comunicação com a AT a partir de uma BD neutralizada. Comportamento **correto e desejado**;
não deve ser "corrigido".

Causa concreta: existem **140 séries** (`l10n_pt.account.series`), 138 `active` com código
de validação da AT. A Casper Ventures tem séries 2026 para *Invoice* e *Recibo*, mas
**não para Orçamentos** — ao publicar um orçamento de 2026 o módulo tenta criar a série
via webservice, e a neutralização trava.

### Dois bloqueios INDEPENDENTES (importante)

| # | Bloqueio | Onde bate | Natureza |
|---|---|---|---|
| 1 | Webservice ATCUD (série 2026 de orçamentos em falta) | ao **Publicar** um orçamento | esperado, por design |
| 2 | Contas sem empresa (secção 13) | ao **criar** qualquer fatura | **defeito a corrigir** |

Testado com diário de vendas certificado **e** série 2026 válida: a fatura direta nem
chega ao webservice — rebenta antes com `AccessError` das contas.

**Conclusão prática: resolver o webservice NÃO desbloqueia a faturação.** O bloqueio de
raiz é a secção 13.

### Falsos negativos por dados de teste (não eram bugs)

Os primeiros resultados deste teste eram enganadores por escolha errada de registos:

| Erro | Causa real |
|---|---|
| `ValidationError: Deve existir um e apenas um imposto de IVA por linha` | o artigo do `search(limit=1)` tinha 0 ou 2 impostos |
| `UserError: É necessário definir um local de fornecedor` | fornecedor sem localização configurada |
| `ValidationError: You do not have any allocation for this time off type` | tipo de ausência que exige alocação |

Com um artigo de 1 imposto, um fornecedor de encomendas reais e um tipo de ausência
`requires_allocation='no'`, **Compras e RH passam**. Ver secção 21 para como escolher
dados válidos.

### O `AccessError` NÃO é um problema de permissões
Rastreado: `check_access(read/write/create)` passa em `account.move.line`. A linha herda a
empresa da conta; a conta não tem empresa (`company_ids: []`); a regra multi-company
rejeita. **É a secção 13**, não um bug novo.

**Impacto prático:** não é possível faturar nesta BD enquanto as contas não tiverem empresa.
Esta é a tradução funcional concreta do bloqueio — mais útil do que "account.account
devolve 0 registos".

---

## 21. Metodologia de teste funcional

### O que NÃO chega
Abrir vistas (`get_views`) valida que a vista compila, **não** que a aplicação funciona.
Um varrimento de 545 ações de menu deu 504 OK — e mesmo assim **não se conseguia faturar**
(secção 20). Vistas OK != aplicação funcional.

### Teste de fluxos de negócio
O que apanha problemas reais: **criar -> confirmar -> faturar -> pagar**, em savepoint
revertido no fim (não grava nada):

```python
cr.execute("SAVEPOINT f")
try:
    so = env['sale.order'].create({...}); so.action_confirm()
    inv = so._create_invoices(); inv.action_post()
finally:
    cr.execute("ROLLBACK TO SAVEPOINT f")
```

**Savepoints são obrigatórios num varrimento:** sem eles, o primeiro erro SQL aborta a
transação (`InFailedSqlTransaction`) e todos os testes seguintes falham em cascata,
escondendo os resultados.

### Teste no browser (`quality_test.js`)
O plano de referência do servidor (`/home/adminarxi/odoo19/PLANO_TESTES.md` +
`quality_test.js`, Playwright) foi adaptado para correr localmente em
`/home/adminarxi/odoo19/qtest/`:

- `RESULTS_ROOT` -> `qtest/test-results`, `BASE` -> `http://localhost:8017`
- sessão obtida por RPC para `/tmp/pw-smoke/session_id.txt` (o script não faz login por formulário)
- `npm i playwright-core` + `npx playwright install chromium`

```bash
cd /home/adminarxi/odoo19/qtest
node quality_test.js <job_id> http://localhost:8017 ["App"]   # App opcional, para debug
```

Vantagem sobre o varrimento backend: **descobre as secções lendo a própria UI** (não uma
lista fixa) e **cria registos**, que é onde os bugs de migração aparecem. Produz
`video.webm` + `log.txt` (PT-PT) + `results.json`, com timestamp de vídeo por erro.

### Ruído a ignorar (do plano original)
- Imagens em falta (`/web/image/`, `image_128`, previews de PDF) -> é o filestore
  (secção 3), não regressão de código
- `Failed to load resource:` genérico sem URL -> redundante com o `failedRequests`

### Escolher dados de teste válidos (senão o teste mente)

```python
# artigo com EXACTAMENTE 1 imposto de venda da empresa em teste
[p for p in Produtos.search([('sale_ok','=',True)], limit=400)
   if len(p.taxes_id.filtered(lambda t: t.company_id == empresa)) == 1]

# fornecedor comprovadamente utilizável (já usado em encomendas confirmadas)
env['purchase.order'].search([('state','in',('purchase','done'))], limit=1).partner_id

# tipo de ausência que não exige alocação
env['hr.leave.type'].search([('requires_allocation','=','no')], limit=1)
```

Três das falhas iniciais da secção 20 eram **dados maus, não bugs**.

### Emails numa BD neutralizada

Não sai email real (é o objetivo da neutralização), mas o que apanha regressões **é**
testável — renderizar o template QWeb, porque um campo removido rebenta o corpo do email:

```python
tpl = env.ref('sale.email_template_edi_sale')      # e account.email_template_edi_invoice
body = tpl._render_field('body_html', doc.ids)[doc.id]
subj = tpl._render_field('subject', doc.ids)[doc.id]
```

### Lição: reproduzir antes de corrigir
Confirmado duas vezes nesta migração (`board.board` na secção 16; a primeira hipótese
para o `x_plan7_id` na secção 19): **um "erro" isolado pode ser limitação do próprio
teste, não da aplicação**. Reproduzir à mão antes de mexer em código.

---

## 22. Teste profundo Playwright — 293 ecrãs, 0 regressões

Run completa do `quality_test.js` (ver secção 21 e `PLANO_TESTES.md`) contra
`localhost:8017`.

```
Início 16:07 | Fim 16:52 | Duração 45 min
Itens testados (apps + submenus): 293
RESULTADO: 11 itens com problemas reais
Artefactos: qtest/test-results/run_full_1707/{log.txt, results.json, video.webm (218 MB)}
```

### Os 11 "problemas" — nenhum é regressão de migração

| # | Item | Erro | Verdicto |
|---|---|---|---|
| 1 | Faturação > Analytic Budget | `OwlError` no lifecycle | **já corrigido** — ver abaixo |
| 2 | Faturação > Invoices To Be Issued | `ConnectionLostError` | restart do servidor a meio da run |
| 3 | Contabilidade > (root) | `net::ERR_ABORTED` | o mesmo restart |
| 4-8 | Documentos ×2, Projeto ×3 | "elemento escondido" | cascata do mesmo restart (25:40-26:36) |
| 9-11 | Assiduidades ×2 | timeout de 3s | carga da máquina (browser a competir com a run) |

**Item 1 — o único candidato a bug real:** o `OwlError` ocorreu às **14:10** do vídeo, ou
seja **antes** de as 413 colunas `x_plan*_id` terem sido criadas em `budget_line`
(secção 19, ~17:30). Revalidado depois no browser: a lista abre, o botão **Novo** abre o
formulário sem erros, e as *Linhas do Orçamento* mostram as colunas dos planos analíticos
(Office, Portfolio, Startups, Real Estate, Crypto, ...) — exactamente as colunas criadas
pela correção. **Já não reproduz.**

### `create=no "new" button found` — 106 ocorrências, 3 causas legítimas

O relatório não distingue *"o botão não devia existir"* de *"o botão existe mas o script
não o encontra"*. Investigados por inspeção (ver `PLANO_TESTES.md`):

| Exemplo | Causa | Correto? |
|---|---|---|
| Revisão > Itens do Diário | `create="false"` no arch da vista | sim (não se criam movimentos à mão) |
| Para Faturar > Encomendas/Upselling | `context: {'create': False}` na ação | sim (listas de trabalho sobre registos existentes) |
| Vendas > Equipas | nenhuma das duas | **limitação do script** — `create()` funciona (testado: id=23) |

### Nota de diagnóstico: separador do browser corrompido

Durante a investigação, o separador do Chrome passou a devolver `body` com 655 bytes e
`.o_action_manager = null` em **todas** as páginas — parecia falha grave da aplicação.
Era o **separador**, degradado após horas de uso: num separador novo tudo renderiza.
Confirmado por RPC em paralelo (HTML 13,6 KB + bundle JS 9,2 MB válidos).

**Ao ver "ecrã em branco" no browser, validar sempre por RPC antes de concluir que é bug
da aplicação.**

---










## Comandos úteis

```bash
# arrancar
cd /home/adminarxi/odoo19
./.venv/bin/python odoo-server/odoo-bin -c custom/config/admincore-arxi.conf \
    -d admincore_19_1 --db-filter='^admincore_19_1$'

# parar (pkill pelo nome da conf mata a própria shell; usar o PID da porta)
kill $(ss -ltnp | grep 8017 | grep -oP 'pid=\K[0-9]+')

# recarregar assets de um módulo depois de mexer no manifest
./.venv/bin/python odoo-server/odoo-bin -c custom/config/admincore-arxi.conf \
    -d admincore_19_1 -u <modulo> --stop-after-init

# forçar reconstrução dos assets (se voltar a dar erro de JS)
psql -d admincore_19_1 -c \
  "DELETE FROM ir_attachment WHERE res_model='ir.ui.view' AND name LIKE '%assets%';"
```

## Diagnóstico — resíduos v17 na BD

O padrão recorrente desta migração é **a BD trazer valores da v17 que o código v19 já não
aceita**. Corrigir só o ficheiro XML/Python não chega: o Odoo lê e valida o que está na BD.

```sql
-- 'tree' onde a v19 espera 'list'  (secção 12)
SELECT count(*) FROM ir_act_window      WHERE view_mode LIKE '%tree%';
SELECT count(*) FROM ir_act_window_view WHERE view_mode = 'tree';
SELECT count(*) FROM ir_ui_view         WHERE arch_db::text LIKE '%<tree%';

-- translate com string 'false'/'true' em vez de NULL/'standard'  (secção 11b)
SELECT translate, count(*) FROM ir_model_fields GROUP BY translate;

-- campos renomeados na v19 ainda em archs  (secção 9)
SELECT count(*) FROM ir_ui_view WHERE arch_db::text ~ '(^|[^_])inalterable_hash';

-- campos removidos na v19 ainda usados em código custom  (secção 15)
--   res.groups.category_id -> privilege_id.category_id
--   res.groups.trans_implied_ids -> all_implied_ids
grep -rn "category_id\|trans_implied_ids\|get_application_groups" --include=*.py .

-- contas sem empresa: DEVE ser ~= nº de contas, se der 0 é a secção 13
SELECT (SELECT count(*) FROM account_account) AS contas,
       (SELECT count(*) FROM account_account_res_company_rel) AS ligacoes;

-- manifests que ficaram em 17.0/18.0  (secção 11c)
--   usar ast.literal_eval, NÃO regex: há manifests com aspas duplas
find . -name __manifest__.py -not -path "*__pycache__*" | while read f; do
  python3 -c "import ast;m=ast.literal_eval(open('$f').read());v=m.get('version','?');
print(v,'$f') if not str(v).startswith('19') else None"
done
```
