## Relatório automático da migração Odoo 17 → 19

Gerado automaticamente pelo motor de migração em 2026-08-24 11:45:39 UTC.

- **Cliente:** admincore
- **Branch:** `migration-v17-to-v19-20260820000635`
- **URL de teste:** http://localhost:8019/web?db=admincore
- **28 correções automáticas** aplicadas ao código durante esta migração (lista completa abaixo).

### Módulos desativados / fora do âmbito desta migração

Marcados como não instalados no v19 — dados preservados na base de dados, só o código não corre nesta versão:

- `hr_contract`
- `hr_contract_reports`
- `hr_contract_sign`
- `base_automation_hr_contract`
- `hr_appraisal_contract`
- `hr_holidays_contract_gantt`
- `planning_contract`
- `project_enterprise_hr_contract`
- `spreadsheet_dashboard_hr_contract`
- `hr_work_entry_contract`
- `hr_work_entry_contract_attendance`
- `hr_work_entry_contract_enterprise`
- `hr_work_entry_contract_planning`
- `documents`
- `documents_spreadsheet_crm`
- `documents_fleet`
- `documents_hr_expense`
- `documents_hr_payroll`
- `documents_project_sign`
- `documents_approvals`
- `documents_hr_contract`
- `documents_project_sale`
- `hr_payroll`
- `hr_payroll_account`
- `hr_payroll_account_sepa`
- `hr_payroll_attendance`
- `hr_payroll_fleet`
- `hr_payroll_holidays`
- `hr_payroll_planning`
- `spreadsheet_dashboard_hr_payroll`
- `project_hr_payroll_account`
- `l10n_pt_hr_payroll`
- `l10n_pt_payroll_unique_report`
- `payroll_arxi`
- `l10n_mz_hr_payroll`
- `admincore_salary_structures`
- `arxi_openai_client`
- `l10n_pt_ao_sale_subscription`

### Correções automáticas aplicadas ao código (histórico completo, mais recente primeiro)

Cada linha corresponde a um commit real nesta branch, feito automaticamente pelo motor para resolver uma incompatibilidade concreta entre o Odoo 17 e o 19:

- `3b4c1f2` (2026-08-24 11:44) auto-fix v19: sincroniza correções aplicadas ao vivo nesta sessão (user_menu_visibility groups_id/create_action, deferrals_option menus órfãos, admin_expiration_panel useService)
- `9126de9` (2026-08-20 00:39) auto-fix v19: filtra country_id.code em Python (campo deixou de ser stored no Odoo 19) em post-update_chart_template.py (iteração 17)
- `4603a2d` (2026-08-20 00:38) auto-fix v19: remove campo 'reversal_move_id' (removido do modelo core) em account_asset_views.xml (iteração 16)
- `d66d974` (2026-08-20 00:06) chore: normaliza estrutura para v19 (renomeia ficheiros '~', corrige versão do manifesto)
- `b024900` (2026-08-19 20:36) fix(casperventures): xmlid morto invoice_shipping_info.report_invoice_document -> l10n_pt_certificate.report_invoice_document (invoice_shipping_info absorvido, uninstalled na migração v19)
- `8811567` (2026-08-19 19:55) fix(casperventures): odoo.fields no longer reexports datetime in v19 (use stdlib datetime)
- `7074ffc` (2026-08-19 18:17) casperventures: remove bank_rec_widget.py — modelo bank.rec.widget removido/redesenhado no v19 (account_accountant), enforcement de distribuição analítica já coberto genericamente por account_move.py::_post() para todos os journal entries (não dependia do wizard)
- `0038636` (2026-08-19 17:35) casperventures: remove import morto de find_xml_value (odoo.tools) — v19 já não reexporta esse símbolo no top-level (só em odoo.tools.xml_utils), símbolo nunca usado no ficheiro
- `e3c101a` (2026-08-19 12:26) fix: desativa l10n_pt_ao_sale_subscription (bug real @depends product_uom->product_uom_id v19, nao PyArmor)
- `daeace3` (2026-08-19 11:56) fix: reverte installable=True indevido em arxi_openai_client (binario PyArmor nao recompilado)
- `0c63f44` (2026-08-19 11:43) fix: reverte 'installable': False acidental em 36 módulos que a Arxi já tinha corrigido (PyArmor Python 3.12) em 6e30f65, mas o merge 41a25a7 (2026-08-14) resolveu o conflito a favor da versão local desatualizada
- `a675298` (2026-08-19 10:22) fix: post-migrate_set_proforma_server_action_groups.py de l10n_pt_ao_sale escrevia 'groups_id' em ir.actions.server, campo renomeado para 'group_ids' no Odoo 19 (ValueError: Invalid field 'groups_id' ao carregar a migração 1.15, rebentava o registry inteiro)
- `874a40a` (2026-08-19 06:18) l10n_pt_ao: add missing 'sale' depend (account.move.downpayment_origin needs sale.order registered before load)
- `a199d4a` (2026-08-19 03:05) fix: pre-merge_absorbed_modules.py de l10n_pt_ao apagava invoice_shipping_info.report_invoice_document sem apagar primeiro a vista filha (casperventures.report_goods_available_brainr) que a herda via inherit_id, violando ir_ui_view_inherit_id_fkey — reusa o padrão recursivo já usado em ../1.1/pre-migration.py para apagar a vista e todos os descendentes antes do commit da BD
- `bee69d5` (2026-08-19 02:35) fix: pre-migration.py de l10n_pt_ao apagava report_custom_invoice_document sem apagar primeiro a vista filha (casperventures.override_narration_custom_report) que a herda via inherit_id, violando ir_ui_view_inherit_id_fkey — apaga a vista e todos os descendentes (recursivo) antes do commit da BD
- `80a5171` (2026-08-18 23:49) fix: contract_instance_checker foi apagado por completo pelo bundle de certificação v19 da Arxi (commit 6e30f65) sem substituto — remove o depend morto de l10n_pt_ao; adapta casperventures de hr.contract (removido no v19, fundido em hr.version) para hr.version, incluindo o filtro state=='open' -> is_current e as referências de xmlid/res_model
- `691d1b8` (2026-08-14 12:27) fix: xpath //header já não existe na vista de product.template no Odoo 19 (vista reestruturada) — usa //form como âncora, mesmo efeito
- `41a25a7` (2026-08-14 12:17) Merge: binários PyArmor recompilados para Python 3.12 pela Arxi (commit 6e30f65, DiogoCarreira) com o trabalho local desta sessão
- `14a9e6a` (2026-08-14 11:25) fix: desacopla product_sale_history do account_taxcloud (módulo Enterprise descontinuado no Odoo 19) — remove depends e a vista que dele dependia, mantém os campos e a lógica de negócio reais intactos
- `925e3ba` (2026-08-13 17:07) fix: Odoo 19 renomeou <tree> para <list> nas vistas — corrige ParseError em deferrals_option e outros módulos próprios que usavam a tag/view_mode antiga
- `e8cf4ec` (2026-07-31 14:46) Corrigir tree->list em hr_attendance_reason (nó raiz de vista list deve ser <list> em v19)
- `8dd9d09` (2026-07-31 13:24) Remover campo category_id (removido de res.groups em v19, substituído por privilege_id/res.groups.privilege, modelo diferente sem equivalente direto) em internal_portal_attendances
- `66be4a9` (2026-07-31 09:49) Corrigir import de Intervals removido de resource.models.utils em v19 (movido para odoo.tools.intervals) em planning_automatic_timesheets
- `637ee9f` (2026-07-30 07:55) Substituir ormcache_context obsoleto (removido em v19) por ormcache com contexto explícito em user_menu_visibility
- `21e6377` (2026-07-30 07:49) Remover decorator @api.returns obsoleto (removido do odoo.api em v19) em user_menu_visibility
- `9256ef1` (2026-07-30 07:44) Corrigir import 'registry' removido do odoo top-level em v19 (não usado, só import morto) em 2 módulos
- `80f81ed` (2026-07-30 07:36) Desativar temporariamente todos os módulos PyArmor incompatíveis com Python 3.12 (Odoo 19)
- `4ac8cb0` (2026-07-30 07:32) Desativar arxi_openai_client temporariamente (binario PyArmor incompativel com Python 3.12 do Odoo 19)
