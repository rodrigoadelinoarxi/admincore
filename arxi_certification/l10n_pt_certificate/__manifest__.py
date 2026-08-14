{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'                 : 'Portugal - Certified Invoicing',
    'summary'              : """
        Module for certified invoicing and exporting SAF-T""",
    'author'               : "ARXILEAD",
    'website'              : "https://www.arxi.pt",
    'category'             : 'Accounting & Finance',
    'sequence'             : 150,
    'version'              : '19.0.1.0.97',
    'license'              : 'OPL-1',
    'depends'              : [
        'account',
        'l10n_pt_ao',
        'l10n_pt_ao_access',
        'l10n_pt_ao_saft',
        'sh_message',
    ],
  
    'external_dependencies': {
        'python': ['pycryptodome', 'xmlschema', 'pdftotext', 'zeep'],
    },
    'data'                 : [
        # Security
        'security/ir.model.access.csv',
        'security/ir_rule.xml',

        # Data
        'data/account_tax_exemption.xml',
        'data/account_taxonomy_data.xml',
        'data/document_status_type.xml',
        'data/income_data.xml',
        'data/config_param.xml',
        'data/res_partner_data.xml',
        'data/account_document_type.xml',
        'data/saft_template.xml',
        'data/cius_pt_templates.xml',
        'data/ubl_templates_cius_pt.xml',
        'data/res.lang.csv',

        # Report
        'report/account_move_templates.xml',
        'report/report_templates.xml',
        'report/account_payment_templates.xml',

        # Views
        'views/account_move_views.xml',
        'views/account_journal_views.xml',
        'views/account_payment_views.xml',
        'views/res_company_views.xml',
        'views/account_tax_views.xml',
        'views/account_series_views.xml',
        'views/res_config_settings_views.xml',
        'views/account_income_type_views.xml',
        'views/account_income_location_views.xml',
        'views/account_taxonomy.xml',
        'views/res_partner_views.xml',
        'views/l10n_pt_certificate_menus.xml',
        'views/account_account.xml',
        'views/uom_uom_views.xml',

        # Wizard
        'wizard/account_payment_views.xml',
        'wizard/saft_wizard_views.xml',
        'wizard/saft_import_wizard_views.xml',
        # 'wizard/account_invoice_send_views.xml',
        'wizard/account_series_wizard_views.xml',
        'wizard/update_tax_grid_wizard_views.xml',
    ],
    'demo'                 : [
        'demo/demo_company.xml',
    ],
    'assets'               : {
        'web.report_assets_common': [
            'l10n_pt_certificate/static/src/scss/reports.scss',
        ],
    },
    'pre_init_hook'        : '_pre_init_hook',
    'post_init_hook'       : '_post_init_hook'
}
