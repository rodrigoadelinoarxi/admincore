# Ledger de Migração — admincore_sh v19 (Odoo.sh)

Registo das correções feitas para ativar Enterprise + módulos próprios na base
`admincore_sh` depois do upgrade oficial 17→19 via `upgrade.odoo.com`.

- **BD:** `admincore_sh` (container `admincore_sh_19_db`)
- **Instância:** `admincore_sh_19_odoo` (imagem própria `admincore_sh_19_odoo_custom`,
  ver `Dockerfile` em `/opt/odoo-migrations/projects/admincore_sh/real_odoo19/`)
- **URL:** https://10.10.10.88:9021/odoo
- **Login:** `administradorARXI` / `Admin1234!`
- **Data:** 2026-08-31
- **Contrato Odoo.sh:** M22052340091004

## Resumo

| # | Assunto | Estado |
|---|---|---|
| 1 | `account.payment` sem `payment_method_line_id` (constraint nativa) | **RESOLVIDO** (SQL, ver `migrate.sh`) |
| 2 | `account.payment` com linha de outro diário | **RESOLVIDO** (SQL, ver `migrate.sh`) |
| 3 | Menu órfão `tax_exemptions` (falso positivo no teste de upgrade) | **RESOLVIDO** (SQL, ver `migrate.sh`) |
| 4 | `pg_dump` remoto do script oficial (`-d`) incompatível com o nosso Postgres | **RESOLVIDO** (contornado, usar sempre `-i`) |
| 5 | `static/description/index.html` com declaração XML rebenta lxml v19 | **RESOLVIDO** (código) |
| 6 | `account.tax_groups_totals` descontinuado (`shared_tax_totals_brainr.xml`) | **DESATIVADO** (cosmético) |
| 7 | `l10n_pt_ao.report_custom_invoice_document` — narração mudou de estrutura | **DESATIVADO** (cosmético) |
| 8 | `inalterable_hash` → `pt_arxi_inalterable_hash` (l10n_pt_sale) | **RESOLVIDO** (código) |
| 9 | `div[@name='signature']` removido do template nativo | **DESATIVADO** (sem impacto) |
| 10 | Reposicionamento custom do QR Code/ATCUD (`sale_qrcode_position_fix`) | **DESATIVADO** (QR/ATCUD nativo continua a aparecer) |
| 11 | `tree` → `list` (rename do framework, `sale_views.xml`) | **RESOLVIDO** (código) |
| 12 | `account_followup.action_view_list_customer_statements` removido | **DESATIVADO** (sem equivalente) |
| 13 | Vista órfã `l10n_pt_reports_arxi` com campo `l10n_pt_cope_exclude` removido | **RESOLVIDO** (SQL, na BD) |
| 14 | Cluster de módulos PyArmor/payroll/documents preso em `to upgrade` | **RESOLVIDO** (SQL, na BD) |
| 15 | Referências a `doc.inalterable_hash` em código novo (não-XPath) de `sale_custom_report_brainr.xml` | **por resolver** (só dá erro se o `t-if`/`t-value` for avaliado ao imprimir) |
| 16 | Vistas Studio com campos removidos (`sale.order.or_is_subscription`, `hr.salary.rule.income_type`, `sale.order.template.spreadsheet_template_id`) | **por resolver** (Odoo desativa-as sozinho, aviso não fatal) |

---

## 1-3. `account.payment` sem/errado `payment_method_line_id` + menu órfão `tax_exemptions` — RESOLVIDO

Estas 3 correções são aplicadas **na base de dados**, não no código deste repo — vivem
como funções reutilizáveis em `/opt/odoo-migrations/engine/migrate.sh`
(`fix_missing_payment_method_line_id` linha 1540, `fix_stale_payment_method_line_journal`
linha 1577, `fix_stale_tax_exemptions_menu` linha 1635), chamadas automaticamente pelo
motor antes de qualquer teste/produção Odoo.sh. Ver comentários extensos nessas funções
para diagnóstico completo (35 pagamentos sem linha, 15 com linha do diário errado, menu
`tax_exemptions.account_tax_exemption_menu_action` órfão a causar falso positivo no
crawler de teste do upgrade oficial).

## 4. `pg_dump` remoto do script oficial incompatível — RESOLVIDO

O modo `-d DBNAME` do `upgrade.odoo.com` (ele próprio faz `pg_dump` remotamente) dava um
erro falso `ir_module_category is not FK on itself`. Corrigido em `migrate.sh`
(`cmd_upgrade_odoo_sh`): gerar sempre o dump localmente com o nosso `pg_dump` e enviar via
`-i ficheiro.sql`, nunca `-d`.

## 5. `static/description/index.html` com declaração XML — RESOLVIDO

`hr_attendance_reason/static/description/index.html` e
`hr_attendance_autoclose/static/description/index.html` começavam com
`<?xml version="1.0" encoding="utf-8" ?>` — o `lxml` do Odoo 19 rejeita essa declaração em
strings unicode (`_get_desc()` em `ir_module.py` decodifica para `str` antes de fazer
parse). Correção: removida a primeira linha em ambos os ficheiros (cosmético, só afeta a
ficha do módulo na loja de apps).

## 6. `account.tax_groups_totals` descontinuado — DESATIVADO

`casperventures/reports/shared_tax_totals_brainr.xml`, template
`shared_tax_groups_totals_inherit`: herdava de `account.tax_groups_totals`, xmlid que já
não existe no Odoo 19 — a estrutura antiga `amount_by_group` foi substituída por
`tax_totals`/`subtotals` em `account.document_tax_totals_template`. Não é um simples
rename (estrutura de dados diferente). Efeito da desativação: perde-se a troca cosmética
de label "IVA"→"Tax" nos totais de imposto nos relatórios; sem impacto nos valores.
Precisa de reescrita manual contra a nova estrutura se se quiser recuperar.

## 7. Narração do `l10n_pt_ao` mudou de estrutura — DESATIVADO

`casperventures/reports/account_custom_report_brainr.xml`, template
`override_narration_custom_report`: XPath `span[@name='comment'][@t-field='o.narration']`
já não existe — a narração passou a viver dentro de
`<div name="comment">...<span t-field="o.narration"/></div>` (sem o atributo `name` no
span), e esse div já tem a sua própria condição de visibilidade nativa. Efeito: perde-se
só a condição extra `not o.company_id.use_custom_report` desta customização.

## 8. `inalterable_hash` renomeado — RESOLVIDO

`casperventures/reports/sale_custom_report_brainr.xml`, template
`sale_remove_not_certified`: o campo `inalterable_hash` foi renomeado para
`pt_arxi_inalterable_hash` no `l10n_pt_sale` v19. XPath atualizado para o novo nome,
comportamento mantido (remove o texto "Document Not Certified" quando o documento já
tem hash).

## 9-10. `signature` removido / QR Code reposicionado — DESATIVADOS

Mesmo ficheiro `sale_custom_report_brainr.xml`:
- `div[@name='signature']` não existe no template PDF nativo do Odoo 19 (a assinatura só
  vive no portal agora, via módulo `sign`) — bloco de "esconder assinatura" desativado,
  sem impacto real (a assinatura já não existia no PDF de qualquer forma).
- `sale_qrcode_position_fix`: reposicionava o QR Code/ATCUD para a direita, mas
  `div[@name='atcud_qr_code']` foi substituído por chamadas a
  `l10n_pt_sale.qr_code_container_sale_order` (mudança estrutural). **O QR Code e o ATCUD
  continuam a aparecer no documento** via template nativo — só o alinhamento/estilo custom
  à direita é que se perde. Sem impacto de certificação fiscal.

## 11. `tree` → `list` — RESOLVIDO

`casperventures/views/sale_views.xml`: `//field[@name='order_line']/tree//...` →
`.../list//...`. Rename padrão do framework Odoo 17+ (`<tree>` passou a `<list>`),
comportamento mantido.

## 12. Ação `account_followup` removida — DESATIVADO

`casperventures/views/account_journal_dashboard_views.xml` +
`account_followup_views.xml`: `account_followup.action_view_list_customer_statements` e
`account_followup.customer_statements_menu` foram removidos do módulo Enterprise
`account_followup` no v19 (só sobram como strings residuais em `.po`, sem equivalente
direto de "Customer Statements"). Perde-se o atalho "Billing Reports" no dashboard de
diários. Precisa de decisão de negócio se se quiser recuperar (ligar a outro
relatório/ação).

## 13. Vista órfã com campo removido — RESOLVIDO (SQL na BD)

`l10n_pt_reports_arxi.view_account_journal_form_l10n_pt_reports_arxi` (ir.ui.view id 6088
na BD `admincore_sh`, sem correspondência no código fonte atual, de julho) referenciava
`l10n_pt_cope_exclude`, campo removido de `account.journal`. Neutralizada por SQL
(`arch_db = '<data/>'`) — não existe em nenhum ficheiro deste repo, é resíduo antigo.

## 14. Cluster PyArmor/payroll/documents preso em `to upgrade` — RESOLVIDO (SQL na BD)

27 módulos com `installable: False` (o mesmo cluster documentado desde a migração do
`admincore` on-premise — `documents*`, `l10n_pt_hr_payroll`, `arxi_openai_client`,
`sh_message`, etc.) + 5 em cascata (`admincore_salary_structures`, `ai_documents`,
`ai_documents_account`, `ai_documents_source`, `spreadsheet_sale_management`) ficaram
presos em `state='to upgrade'` depois do `-u all` (o `module_graph` salta-os como "not
installable" antes de decidir o estado final). Como 'to upgrade' ≠ 'uninstalled', as
vistas deles continuavam ativas e combinadas em ecrãs partilhados (ex.: Definições),
causando `OwlError: field is undefined` no browser. Corrigido por SQL:
`state='uninstalled'` + `active=false` nas suas `ir_ui_view`.

## 15-16. Pendências para revisão humana

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
