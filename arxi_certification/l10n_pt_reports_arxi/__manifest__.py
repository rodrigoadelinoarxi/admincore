{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'         : 'Portugal - Accounting Reports',
    'icon'         : '/l10n_pt_certificate/static/description/icon.png',
    'version'      : '19.0.1.0.60',
    'summary'      : 'Accounting reports for Portugal',
    'category'     : 'Accounting/Localizations/Reporting',
    'depends'      : ['l10n_pt_arxi_coa', 'l10n_pt_certificate', 'l10n_pt_ao_reports', 'account_asset_law'],
    'data'         : [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/account.bank.identifier.csv',
        'data/account.statistical.classification.csv',
        'data/account.account.tag.csv',
        'data/account_report_xml_struct.xml',
        'data/account_tags_data.xml',
        'data/tax_report_refund_type_data.xml',
        'data/tax_report_template_xml.xml',
        'data/account_tax_report.xml',
        'data/profit_loss.xml',
        'data/balance_sheet.xml',
        'data/asset_report_annex_32.xml',
        'data/cash_flow_statement_report.xml',
        'data/account_report_annex_40.xml',
        'data/account_report_annex_41.xml',
        'data/analytic_ledger.xml',
        'data/cash_flow.xml',
        'data/account_report_annex_customers.xml',
        'data/account_report_annex_r.xml',
        'data/account_report_annex_suppliers.xml',
        'data/account_report_model_10.xml',
        'data/account_report_model_10_table_5.xml',
        'data/statement_of_changes_in_equity_report.xml',
        'data/account_report_recapitulativa.xml',
        'data/account_cope_report.xml',
        'data/cope_export_template.xml',
        'data/tax_recap_export_template.xml',
        'data/account.model30.taxation.regimen.csv',
        'data/account.model30.income.type.csv',
        'data/account_report_model_30.xml',
        'data/account_report_model_30_table_7.xml',
        'data/account_report_model_30_table_8.xml',

        # Views
        'views/report_views.xml',
        'views/l10n_pt_reports_arxi_menus.xml',
        'views/account_tax_views.xml',
        'views/account_move_views.xml',
        'views/account_journal_views.xml',
        'views/res_config_settings_views.xml',
        'views/account_report_xml_struct_views.xml',
        'views/account_bank_identifier_views.xml',
        'views/account_statistical_classification_views.xml',
        'views/res_bank_views.xml',
        'views/res_country_views.xml',

        # Wizard
        'wizard/tax_report_export_wizard_view.xml',
        'wizard/cope_report_export_views.xml',
        'wizard/tax_recap_export_wizard_view.xml',
        'wizard/model10_export_wizard_view.xml',

        'report/asset_report_main_table_body.xml',
        'report/asset_report_main_table_header.xml',
    ],

    'assets'       : {
        'web.assets_backend': [
            'l10n_pt_reports_arxi/static/src/components/**/*',
        ],
    },

    'auto_install' : False,
    'license'      : 'OPL-1',
    'pre_init_hook': '_setup_account_tax_closing_transient_account_id',
}
