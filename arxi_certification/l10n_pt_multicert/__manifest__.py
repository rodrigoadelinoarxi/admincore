{
    'name'          : 'Portugal - Invoice Signature',
    'summary'       : """Signs invoices with Multicert.""",
    'author'        : "ARXILEAD",
    'website'       : "https://www.arxi.pt",
    'category'      : 'Accounting & Finance',
    'version'       : '17.0.0.0.2',
    'license'       : 'OPL-1',
    'depends'       : [
        'account_edi',
        'l10n_pt_certificate'
    ],
    'data'          : [
        'data/account_edi_data.xml',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml'
    ],
    'demo': [
        'demo/res_company_demo.xml',
    ],
    'post_init_hook': 'post_init',
}
