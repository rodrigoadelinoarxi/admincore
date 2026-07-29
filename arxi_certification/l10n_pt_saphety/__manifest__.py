{
    'name'          : 'Portugal - Saphety Invoice Signature',
    'summary'       : """Signs invoices with Saphety.""",
    'author'        : "ARXILEAD",
    'website'       : "https://www.arxi.pt",
    'category'      : 'Accounting & Finance',
    'version'       : '17.0.0.0.23',
    'license'       : 'OPL-1',
    'depends'       : [
        'account_edi',
        'l10n_pt_certificate',
        'l10n_pt_edi_partner_filter',
    ],
    'data'          : [
        'security/ir.model.access.csv',
        'data/account_edi_data.xml',
        'data/ir_cron.xml',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml',
        'views/product_category_views.xml',
        'views/res_company_views.xml',
    ],
    'post_init_hook': '_post_init_hook',
}
