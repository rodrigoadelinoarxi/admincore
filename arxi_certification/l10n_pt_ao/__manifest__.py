{
    'name'                 : 'Invoicing  - Portugal / Angola',
    'summary'              : """
        Module for common invoicing requirements between Portuguese and Angolan localizations""",
    'author'               : "ARXILEAD",
    'website'              : "https://www.arxi.pt",
    'category'             : 'Accounting & Finance',
    'version'              : '17.0.1.0.87',
    'license'              : 'OPL-1',
    'depends'              : [
        'automatic_refs',
        'account_cancel_reason',
        'base_vat',
        'tax_exemptions',
        'auth_password_policy_signup',
        'restrict_update_company_info',
        'invoice_shipping_info',
        'print_conf_copies',
        'contract_instance_checker',
    ],
    'external_dependencies': {
    },
    'data'                 : [
        'security/ir.model.access.csv',
        'security/res_groups.xml',

        'data/config_param.xml',
        'data/payment_mechanism_data.xml',

        'report/report_templates.xml',
        'report/account_move_templates.xml',
        'report/account_payment_templates.xml',
        'report/report_warning.xml',

        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/res_company_views.xml',
        'views/account_journal_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
        'views/account_document_type_views.xml',
        'views/account_move_reversal_view.xml',
        'views/payment_mechanism_views.xml',
        'views/tax_report_refund_type_views.xml',
        'views/res_config_settings_views.xml',
        'views/l10n_pt_ao_menus.xml',
        'views/account_account.xml',
        'views/ir_actions_report_views.xml',

        'wizard/warning_wizard_views.xml'
    ],
    'demo'                 : [
    ],
    'assets'               : {
        'web.assets_backend'      : [
            'l10n_pt_ao/static/src/**/*',
        ],
        'web.report_assets_common': [
            'l10n_pt_ao/static/src/scss/reports.scss',
        ]
    },
    'application'          : True,
    'post_init_hook'       : 'post_init_hook'
}
