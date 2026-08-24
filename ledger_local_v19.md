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
| 10 | `product_uom` -> `product_uom_id` em `l10n_pt_sale` | por resolver (é `arxi_certification`) |

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
- Todas as versões dos manifests bumpadas para `19.0.*`.
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

## 10. `product_uom` -> `product_uom_id` em `l10n_pt_sale` — POR RESOLVER

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

Impacto: o relatório de sale order não renderiza. Requer autorização para mexer em
código de certificação.

### Nota — `wkhtmltopdf` em falta
`_render_qweb_pdf` falha com "Não é possível localizar Wkhtmltopdf neste sistema".
É limitação do ambiente local, não da migração. O render em HTML funciona.

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
