# Ledger de Migração — admincore_sh v19 (Odoo.sh)

Registo das correções feitas na migração 17→19 do `admincore_sh`, dividido em duas
fases distintas:

- **Fase A** — erros encontrados **durante o próprio script de upgrade oficial da Odoo**
  (`upgrade.odoo.com`, comando `upgrade.py test`/`production`), antes de o pedido `production`
  ser sequer aceite/completado. Correções aplicadas à **base de origem**, para o script
  oficial conseguir processar a base sem rebentar.
- **Fase B** — erros encontrados **depois** do upgrade oficial já ter devolvido a base em
  v19 com sucesso, ao ativar os módulos Enterprise + próprios do cliente (que o serviço da
  Odoo não vê, por serem código privado) via `odoo -u all`. Correções no **código deste
  repo** e na **base já migrada**.

- **BD:** `admincore_sh` (container `admincore_sh_19_db`)
- **Instância:** `admincore_sh_19_odoo` (imagem própria `admincore_sh_19_odoo_custom`,
  ver `Dockerfile` em `/opt/odoo-migrations/projects/admincore_sh/real_odoo19/`)
- **URL:** https://10.10.10.88:9021/odoo
- **Login:** `administradorARXI` / `Admin1234!`
- **Data:** 2026-08-31
- **Contrato Odoo.sh:** M22052340091004

## Resumo

### Fase A — durante o script oficial `upgrade.odoo.com`

| # | Assunto | Estado |
|---|---|---|
| A1 | `account.payment` sem `payment_method_line_id` (constraint nativa) | **RESOLVIDO** (SQL na base de origem, ver `migrate.sh`) |
| A2 | `account.payment` com linha de método de pagamento de outro diário | **RESOLVIDO** (SQL na base de origem, ver `migrate.sh`) |
| A3 | Menu órfão `tax_exemptions` (falso positivo no crawler de teste do upgrade oficial) | **RESOLVIDO** (SQL na base de origem, ver `migrate.sh`) |
| A4 | `pg_dump` remoto do próprio script oficial (`-d`) incompatível com o nosso Postgres | **RESOLVIDO** (contorno de invocação, usar sempre `-i`) |

### Fase B — depois do upgrade oficial, ao ativar Enterprise + módulos próprios

| # | Assunto | Estado |
|---|---|---|
| B1 | `static/description/index.html` com declaração XML rebenta lxml v19 | **RESOLVIDO** (código) |
| B2 | `account.tax_groups_totals` descontinuado (`shared_tax_totals_brainr.xml`) | **DESATIVADO** (cosmético) |
| B3 | `l10n_pt_ao.report_custom_invoice_document` — narração mudou de estrutura | **DESATIVADO** (cosmético) |
| B4 | `inalterable_hash` → `pt_arxi_inalterable_hash` (l10n_pt_sale) | **RESOLVIDO** (código) |
| B5 | `div[@name='signature']` removido do template nativo | **DESATIVADO** (sem impacto) |
| B6 | Reposicionamento custom do QR Code/ATCUD (`sale_qrcode_position_fix`) | **DESATIVADO** (QR/ATCUD nativo continua a aparecer) |
| B7 | `tree` → `list` (rename do framework, `sale_views.xml`) | **RESOLVIDO** (código) |
| B8 | `account_followup.action_view_list_customer_statements` removido | **DESATIVADO** (sem equivalente) |
| B9 | Vista órfã `l10n_pt_reports_arxi` com campo `l10n_pt_cope_exclude` removido | **RESOLVIDO** (SQL na base já migrada) |
| B10 | Cluster de módulos PyArmor/payroll/documents preso em `to upgrade` | **RESOLVIDO** (SQL na base já migrada) |
| B11 | Referências a `doc.inalterable_hash` em código novo (não-XPath) de `sale_custom_report_brainr.xml` | **por resolver** (só dá erro se o `t-if`/`t-value` for avaliado ao imprimir) |
| B12 | Vistas Studio com campos removidos (`sale.order.or_is_subscription`, `hr.salary.rule.income_type`, `sale.order.template.spreadsheet_template_id`) | **por resolver** (Odoo desativa-as sozinho, aviso não fatal) |

---

# Fase A — erros do script oficial `upgrade.odoo.com`

Estas 4 correções foram necessárias **antes** de o pedido `production` conseguir
completar. Não tocam em código deste repo — são feitas na base de dados de origem
(pré-upgrade) ou na forma como invocamos o script oficial.

## A1-A3. `account.payment` sem/errado `payment_method_line_id` + menu órfão `tax_exemptions`

A primeira tentativa oficial (2026-08-29) falhou logo com o erro nativo do Odoo
*"Please define a payment method line on your payment"*. Diagnóstico feito num Postgres
Docker temporário com o backup real restaurado:

- 35 registos `account.payment` sem `payment_method_line_id` nenhum.
- 15 registos com a linha preenchida mas a apontar para o diário errado (ou uma linha
  órfã com `journal_id` NULL).
- O menu `tax_exemptions.account_tax_exemption_menu_action` continuava ativo na cópia
  local antes do upgrade (o módulo `tax_exemptions` só fica `installable: False` DEPOIS
  do upgrade), o que fazia o crawler de teste do próprio script oficial registar esse
  menu como "a funcionar antes" e depois falhar a comparação com "depois" (falso
  positivo de regressão, não uma perda real de funcionalidade — já preservada em
  `l10n_pt_ao`).

Estas 3 correções vivem como funções reutilizáveis em
`/opt/odoo-migrations/engine/migrate.sh` (`fix_missing_payment_method_line_id` linha
1540, `fix_stale_payment_method_line_journal` linha 1577,
`fix_stale_tax_exemptions_menu` linha 1635), chamadas automaticamente pelo motor **antes**
de qualquer `test`/`production` Odoo.sh — não é preciso repetir manualmente em migrações
futuras. Ver os comentários extensos nessas funções para o diagnóstico SQL completo.

## A4. `pg_dump` remoto do script oficial incompatível

Mesmo com os dados corrigidos (A1-A3), o pedido `test` continuava a falhar, agora com um
erro diferente e enganador: `ir_module_category is not FK on itself` (a FK existia e era
válida, confirmado por query direta a `pg_constraint`). Causa real: o modo `-d DBNAME` do
script `upgrade.odoo.com` faz o **seu próprio** `pg_dump` remotamente, ligando-se por rede
ao nosso Postgres — o `pg_dump` embutido nesse script não é compatível com a nossa versão
de Postgres 16 Docker, e alguma constraint/metadado não sobrevive à passagem pela rede.

**Corrigido em `migrate.sh` (`cmd_upgrade_odoo_sh`):** gerar sempre o dump localmente com
o nosso próprio `pg_dump` (mesmo container que fez o restauro) e enviar ao script oficial
via `-i ficheiro.sql`, nunca `-d`. Isto corrige o fluxo para todos os clientes Odoo.sh
futuros, não só o admincore_sh.

---

# Fase B — ativação de Enterprise + módulos próprios (pós-upgrade)

O script oficial da Odoo devolveu a base já em v19 com sucesso (`RESULT_ODOO_SH_PRODUCTION=OK`,
2026-08-30). Só tinha os módulos **core/community** carregados — o serviço deles não tem
acesso ao código Enterprise licenciado nem aos módulos próprios do cliente (privados). As
correções desta fase foram feitas **depois**, ao correr `odoo -u all` localmente para
ligar Enterprise + o código deste repo à base já migrada.

## B1. `static/description/index.html` com declaração XML

`hr_attendance_reason/static/description/index.html` e
`hr_attendance_autoclose/static/description/index.html` começavam com
`<?xml version="1.0" encoding="utf-8" ?>` — o `lxml` do Odoo 19 rejeita essa declaração em
strings unicode (`_get_desc()` em `ir_module.py` decodifica para `str` antes de fazer
parse). Correção: removida a primeira linha em ambos os ficheiros (cosmético, só afeta a
ficha do módulo na loja de apps).

## B2. `account.tax_groups_totals` descontinuado

`casperventures/reports/shared_tax_totals_brainr.xml`, template
`shared_tax_groups_totals_inherit`: herdava de `account.tax_groups_totals`, xmlid que já
não existe no Odoo 19 — a estrutura antiga `amount_by_group` foi substituída por
`tax_totals`/`subtotals` em `account.document_tax_totals_template`. Não é um simples
rename (estrutura de dados diferente). Efeito da desativação: perde-se a troca cosmética
de label "IVA"→"Tax" nos totais de imposto nos relatórios; sem impacto nos valores.
Precisa de reescrita manual contra a nova estrutura se se quiser recuperar.

## B3. Narração do `l10n_pt_ao` mudou de estrutura

`casperventures/reports/account_custom_report_brainr.xml`, template
`override_narration_custom_report`: XPath `span[@name='comment'][@t-field='o.narration']`
já não existe — a narração passou a viver dentro de
`<div name="comment">...<span t-field="o.narration"/></div>` (sem o atributo `name` no
span), e esse div já tem a sua própria condição de visibilidade nativa. Efeito: perde-se
só a condição extra `not o.company_id.use_custom_report` desta customização.

## B4. `inalterable_hash` renomeado

`casperventures/reports/sale_custom_report_brainr.xml`, template
`sale_remove_not_certified`: o campo `inalterable_hash` foi renomeado para
`pt_arxi_inalterable_hash` no `l10n_pt_sale` v19. XPath atualizado para o novo nome,
comportamento mantido (remove o texto "Document Not Certified" quando o documento já
tem hash).

## B5-B6. `signature` removido / QR Code reposicionado

Mesmo ficheiro `sale_custom_report_brainr.xml`:
- `div[@name='signature']` não existe no template PDF nativo do Odoo 19 (a assinatura só
  vive no portal agora, via módulo `sign`) — bloco de "esconder assinatura" desativado,
  sem impacto real (a assinatura já não existia no PDF de qualquer forma).
- `sale_qrcode_position_fix`: reposicionava o QR Code/ATCUD para a direita, mas
  `div[@name='atcud_qr_code']` foi substituído por chamadas a
  `l10n_pt_sale.qr_code_container_sale_order` (mudança estrutural). **O QR Code e o ATCUD
  continuam a aparecer no documento** via template nativo — só o alinhamento/estilo custom
  à direita é que se perde. Sem impacto de certificação fiscal.

## B7. `tree` → `list`

`casperventures/views/sale_views.xml`: `//field[@name='order_line']/tree//...` →
`.../list//...`. Rename padrão do framework Odoo 17+ (`<tree>` passou a `<list>`),
comportamento mantido.

## B8. Ação `account_followup` removida

`casperventures/views/account_journal_dashboard_views.xml` +
`account_followup_views.xml`: `account_followup.action_view_list_customer_statements` e
`account_followup.customer_statements_menu` foram removidos do módulo Enterprise
`account_followup` no v19 (só sobram como strings residuais em `.po`, sem equivalente
direto de "Customer Statements"). Perde-se o atalho "Billing Reports" no dashboard de
diários. Precisa de decisão de negócio se se quiser recuperar (ligar a outro
relatório/ação).

## B9. Vista órfã com campo removido (SQL na base já migrada)

`l10n_pt_reports_arxi.view_account_journal_form_l10n_pt_reports_arxi` (ir.ui.view id 6088
na BD `admincore_sh`, sem correspondência no código fonte atual, de julho) referenciava
`l10n_pt_cope_exclude`, campo removido de `account.journal`. Neutralizada por SQL
(`arch_db = '<data/>'`) — não existe em nenhum ficheiro deste repo, é resíduo antigo.

## B10. Cluster PyArmor/payroll/documents preso em `to upgrade` (SQL na base já migrada)

27 módulos com `installable: False` (o mesmo cluster documentado desde a migração do
`admincore` on-premise — `documents*`, `l10n_pt_hr_payroll`, `arxi_openai_client`,
`sh_message`, etc.) + 5 em cascata (`admincore_salary_structures`, `ai_documents`,
`ai_documents_account`, `ai_documents_source`, `spreadsheet_sale_management`) ficaram
presos em `state='to upgrade'` depois do `-u all` (o `module_graph` salta-os como "not
installable" antes de decidir o estado final). Como 'to upgrade' ≠ 'uninstalled', as
vistas deles continuavam ativas e combinadas em ecrãs partilhados (ex.: Definições),
causando `OwlError: field is undefined` no browser. Corrigido por SQL:
`state='uninstalled'` + `active=false` nas suas `ir_ui_view`.

## B11-B12. Pendências para revisão humana

- `sale_custom_report_brainr.xml` ainda tem várias referências a `doc.inalterable_hash`
  (não `pt_arxi_inalterable_hash`) em código NOVO da customização (dentro de `t-if`/
  `t-value`, não em XPath de herança — por isso não bloqueou o `-u all`). Só vai dar erro
  em runtime se algum desses ramos for mesmo avaliado ao gerar um PDF. Precisa de
  `grep -n "doc.inalterable_hash" casperventures/reports/sale_custom_report_brainr.xml` e
  substituir por `pt_arxi_inalterable_hash`.
- Vistas Studio custom (não deste repo, criadas pela UI do cliente) referenciam campos
  removidos: `sale.order.or_is_subscription`, `hr.salary.rule.income_type`,
  `sale.order.template.spreadsheet_template_id`. O Odoo desativa-as automaticamente no
  arranque (aviso `invalid custom view(s) for model ...`, não fatal) — decisão do cliente
  se quer recuperar essas customizações Studio.
