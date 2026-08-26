## Relatório automático da migração Odoo 17 → 19

Gerado automaticamente pelo motor de migração em 2026-08-26 12:18:34 UTC.

- **Cliente:** admincore
- **Branch:** `migration-v17-to-v19-20260826091834`
- **URL de teste:** http://localhost:8019/web?db=admincore
- **36 correções automáticas** aplicadas ao código dos módulos durante esta migração (lista completa abaixo).

### Bugs conhecidos do core do Odoo 19, corrigidos preventivamente

Aplicados sempre, em qualquer migração para esta versão — não são específicos deste cliente nem causados por este backup, são bugs reais do próprio Odoo 19 (não dos módulos do cliente), identificados em runs anteriores e corrigidos no motor antes do upgrade correr:

- `patch_odoo_core_analytic_project_plan_missing_bug`
- `patch_odoo_core_import_error_account_templates_bug`
- `patch_odoo_core_menuitem_missing_action_bug`
- `patch_odoo_core_missing_chart_template_mapping_bug`
- `patch_odoo_core_never_delete_account_account`
- `patch_odoo_core_stale_xmlid_fk_violation_bug`
- `patch_odoo_core_timesheet_plan_field_mismatch_bug`
- `patch_odoo_core_view_inheritance_missing_element_bug`

### Erros de dados detetados durante o upgrade real da base de dados (`-u all`, mecanismo oficial de upgrade de módulos do Odoo)

Problemas concretos encontrados NESTES dados enquanto o Odoo (via `odoo-bin -u all`, o mecanismo oficial de upgrade de módulos — não um script à parte) tentava aplicar as alterações de esquema/dados entre o v17 e o v19. Não são bugs de código dos módulos — são inconsistências nos dados restaurados do backup (índices duplicados, constraints obsoletas, registos que mudaram de módulo, xmlids órfãos ou com o modelo trocado), corrigidas para o Odoo poder recriar o estado correto sozinho:

- **2026-08-26 09:30:57** — Xmlid com modelo trocado detetado (ir_model_data id=11263) — a remover o mapeamento antigo para o Odoo recriar do zero...
- **2026-08-26 09:35:26** — Duplicado em índice único detetado (ir_act_window_view id=2191, constraint 'act_window_view_unique_mode_per_action', colunas=act_window_id, view_mode) — a remover a linha extra para o Odoo recriar...
- **2026-08-26 09:35:48** — Duplicado em índice único detetado (ir_act_window_view id=2192, constraint 'act_window_view_unique_mode_per_action', colunas=act_window_id, view_mode) — a remover a linha extra para o Odoo recriar...
- **2026-08-26 09:37:46** — Xmlid local renomeado dentro do mesmo módulo detetado (account_report_line id=48, tem dados dependentes, 'account_reports.account_financial_report_totalincome0' -> 'account_reports.account_financial_report_operating_income0' via code='INC' em account_reports/data/profit_and_loss.xml) — a mapear em vez de apagar...
- **2026-08-26 09:39:21** — Duplicado em índice único detetado (account_report_expression id=48, constraint 'account_report_expression_line_label_uniq', colunas=report_line_id, label) — a remover a linha extra para o Odoo recriar...
- **2026-08-26 09:41:00** — Duplicado em índice único detetado (ir_config_parameter id=89, constraint 'ir_config_parameter_key_uniq', colunas=key) — a remover a linha extra para o Odoo recriar...
- **2026-08-26 09:41:43** — Duplicado em índice único detetado (ir_act_window_view id=185, constraint 'act_window_view_unique_mode_per_action', colunas=act_window_id, view_mode) — a remover a linha extra para o Odoo recriar...
- **2026-08-26 09:43:21** — CHECK constraint obsoleto detetado (hr_leave_accrual_level.hr_leave_accrual_level_check_dates, referencia 'first_day' que mudou de tipo, já não declarado em nenhum código fonte carregado) — a largar para o Odoo poder converter a coluna...
- **2026-08-26 09:44:14** — Duplicado em índice único detetado (hr_work_entry_type id=9, constraint 'hr_work_entry_type_unique_work_entry_code', colunas=code) — a remover a linha extra para o Odoo recriar...
- **2026-08-26 09:45:00** — Registo nativo relocalizado entre módulos detetado (hr_work_entry_type id=2, tem dados dependentes, xmlid 'hr_work_entry_contract.work_entry_type_leave' -> módulo novo 'hr_work_entry') — a mapear em vez de apagar...
- **2026-08-26 09:45:47** — Registo nativo relocalizado entre módulos detetado (hr_work_entry_type id=3, tem dados dependentes, xmlid 'hr_work_entry_contract.work_entry_type_compensatory' -> módulo novo 'hr_work_entry') — a mapear em vez de apagar...
- **2026-08-26 09:46:36** — Duplicado em índice único detetado (hr_work_entry_type id=4, constraint 'hr_work_entry_type_unique_work_entry_code', colunas=code) — a remover a linha extra para o Odoo recriar...
- **2026-08-26 09:47:25** — Registo nativo relocalizado entre módulos detetado (hr_work_entry_type id=5, tem dados dependentes, xmlid 'hr_work_entry_contract.work_entry_type_unpaid_leave' -> módulo novo 'hr_work_entry') — a mapear em vez de apagar...
- **2026-08-26 09:48:11** — Registo nativo relocalizado entre módulos detetado (hr_work_entry_type id=6, tem dados dependentes, xmlid 'hr_work_entry_contract.work_entry_type_sick_leave' -> módulo novo 'hr_work_entry') — a mapear em vez de apagar...
- **2026-08-26 09:48:57** — Registo nativo relocalizado entre módulos detetado (hr_work_entry_type id=7, tem dados dependentes, xmlid 'hr_work_entry_contract.work_entry_type_legal_leave' -> módulo novo 'hr_work_entry') — a mapear em vez de apagar...

### Módulos desativados / fora do âmbito desta migração

Marcados como não instalados no v19 — dados preservados na base de dados, só o código não corre nesta versão:

- `documents`
- `spreadsheet_edition`
- `documents_account`
- `documents_hr`
- `documents_hr_holidays`
- `documents_hr_recruitment`
- `documents_spreadsheet_crm`
- `documents_fleet`
- `documents_hr_expense`
- `documents_hr_payroll`
- `documents_project_sign`
- `documents_approvals`
- `documents_hr_contract`
- `documents_project_sale`
- `documents_spreadsheet_account`
- `documents_sign`
- `documents_spreadsheet`
- `documents_product`
- `documents_project`
- `mail_smtp_imap_by_company_documents`
- `website_documents`
- `documents_spreadsheet_survey`
- `spreadsheet_dashboard_documents`
- `spreadsheet_dashboard_edition`
- `hr_contract`
- `hr_contract_reports`
- `hr_contract_sign`
- `hr_work_entry_contract`
- `hr_work_entry_contract_attendance`
- `hr_work_entry_contract_enterprise`
- `hr_work_entry_contract_planning`
- `hr_work_entry_contract_planning_attendance`
- `base_automation_hr_contract`
- `hr_appraisal_contract`
- `hr_holidays_contract_gantt`
- `planning_contract`
- `project_enterprise_hr_contract`
- `spreadsheet_dashboard_hr_contract`
- `web_editor`
- `account_sepa`
- `account_taxcloud`
- `sale_account_taxcloud`
- `sale_subscription_taxcloud`
- `website_sale_account_taxcloud`
- `account_consolidation`
- `account_auto_transfer`
- `stock_account_enterprise`
- `account_reports_tax_reminder`
- `sh_import_journal_entry`
- `sh_message`
- `account_payment_term`
- `ir_rule_protected`
- `restricted_settings`
- `sale_async_emails`
- `stock_report_by_country`
- `stock_restrictions`
- `website_form_project`
- `spreadsheet_dashboard_purchase`
- `automatic_refs`
- `tax_exemptions`
- `restrict_update_company_info`
- `invoice_shipping_info`
- `print_conf_copies`
- `print_conf_copies_pt`
- `print_conf_copies_sales`
- `l10n_pt_arxi_coa`
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

### Correções de código aplicadas aos módulos, para carregarem/funcionarem corretamente no Odoo 19 (histórico completo, mais recente primeiro)

Cada linha corresponde a um commit real nesta branch, feito automaticamente pelo motor para resolver uma incompatibilidade concreta de código entre o Odoo 17 e o 19:

- `2b5770b` (2026-08-26 09:56) docs: relatório automático da migração v17→v19 (README_CLAUDE.md)
- `7907070` (2026-08-26 09:50) auto-fix v19: filtra country_id.code em Python (campo deixou de ser stored no Odoo 19) em post-update_chart_template.py (iteração 16)
- `f4a5957` (2026-08-26 09:18) chore: normaliza estrutura para v19 (renomeia ficheiros '~', corrige versão do manifesto)
- `491450a` (2026-08-26 09:18) fix(arxi-quality): recupera contract_instance_checker perdido no merge de 25 ago
- `1055ecd` (2026-08-25 08:38) fix(deferrals_option): funde correções paralelas (account_reports/account_asset_law como depends explícitos, campo reversal_move_ids) trazidas pelo merge da branch de migração
- `d126e6b` (2026-08-25 08:26) fix(casperventures): SQL object + str rebentava _select() de account.invoice.report — Odoo 19 devolve um objeto SQL (composição segura), não uma string; corrigido para SQL('%s, ...', super()._select())
- `0d0dd8e` (2026-08-24 15:03) fix: bump versão do manifesto 17.0.x -> 19.0.x em todos os módulos próprios (30 módulos)
- `602f45f` (2026-08-24 11:47) fix: integra correções de Diogo Carreira (expiration_panel, ir_ui_menu, res_users) já publicadas na branch de migração v19 — mesmo diagnóstico independente do useService("user")/create_action() feito nesta sessão
- `6b24014` (2026-08-20 11:55) fix(admin_expiration_panel): useService("user") rebentava o arranque de TODA a HomeMenu no Odoo 19 ("Service user is not available") — troca para o módulo singleton @web/core/user, que expõe a mesma API (hasGroup) sem depender do sistema de serviços do Owl
- `5f429dc` (2026-08-20 09:06) fix(deferrals_option): corrige menus pais órfãos (account.account_management_menu / account.menu_finance_entries_management já não existem no v19) — reancorados em account.account_account_menu e accountant.account_assets_liabilities_menu, senão caíam como apps de topo na página principal
- `9f11441` (2026-08-20 07:41) fix(user_menu_visibility): res.users.groups_id -> group_ids (renomeado no Odoo 19)
- `e01c428` (2026-08-20 07:40) fix(user_menu_visibility): não rebentar load_menus quando create_action() é recusado (ex.: relatório Planning no Odoo 19)
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
