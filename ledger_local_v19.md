# Ledger de Migração Local — v19 (admincore-arxi)

Registo das correções feitas ao restaurar o dump do servidor externo no ambiente local.

- **BD:** `admincore_19_1`
- **Dump:** `admincore_19_20260824_101022.dump` (pg_dump -Fc, origem PG 16.14, BD `admincore`)
- **Config:** `custom/config/admincore-arxi.conf`
- **Login:** `administradorARXI` / `demo1234` (uid 2)
- **Data:** 2026-08-24

---

## 1. Erro de JS no backend (`JSON.parse`) — RESOLVIDO

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

### Nota — limpeza de assets (feita antes, não era a causa)
Também foram apagados 273 attachments de assets, porque o dump veio **sem filestore**
(107.279 registos em `ir_attachment` para apenas 22 ficheiros em disco) e os bundles
apontavam para ficheiros inexistentes. É uma limpeza legítima e os assets regeneram-se,
mas **não era a causa do erro de JS** — o erro persistiu até corrigir o
`user_menu_visibility`. Se voltar a haver assets corrompidos:

```sql
DELETE FROM ir_attachment WHERE res_model='ir.ui.view' AND name LIKE '%assets%';
```

---

## 2. Anexos de negócio em falta — POR RESOLVER (limitação do dump)

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

## 3. Extensão `pgvector` em falta — SEM IMPACTO

`pg_restore` deu 2 erros:
```
ERROR: extension "vector" is not available
```
Verificado que **não há nenhuma coluna do tipo `vector`** na BD
(`SELECT count(*) FROM information_schema.columns WHERE udt_name='vector'` -> 0).
Sem impacto. Se um dia for preciso: `apt install postgresql-16-pgvector`.

---

## 4. Módulos instalados na BD sem código em disco — POR RESOLVER

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

## 5. Comparação com o código oficial v17 — OK

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
| `user_menu_visibility` | `groups_id` + `create_action()` | **installed** | **CORRIGIDO** (ver secção 1) |
| `internal_portal_attendances` | `groups_id` | **installed** | **CORRIGIDO** (ver secção 1) |
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

## Comandos úteis

```bash
# arrancar
cd /home/adminarxi/odoo19
./.venv/bin/python odoo-server/odoo-bin -c custom/config/admincore-arxi.conf \
    -d admincore_19_1 --db-filter='^admincore_19_1$'

# forçar reconstrução dos assets (se voltar a dar erro de JS)
psql -d admincore_19_1 -c \
  "DELETE FROM ir_attachment WHERE res_model='ir.ui.view' AND name LIKE '%assets%';"
```
