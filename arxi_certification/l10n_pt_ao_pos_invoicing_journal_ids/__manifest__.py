{
    'name'        : 'Portugal / Angola - Certified Point of Sale Select Invoicing Journal',
    'summary'     : """
        Module for POS Select Invoicing Journal""",

    'author'      : "Arxi",
    'website'     : "https://www.arxi.pt",
    'category'    : 'Sales/Point Of Sale',
    'version'     : '17.0.0.0.2',
    'license'     : 'OPL-1',
    'depends'     : [
        'l10n_pt_ao_pos',
    ],
    'data'        : [
        'views/res_config_settings_views.xml'
    ],
    'assets'      : {
        'point_of_sale._assets_pos': [
            'l10n_pt_ao_pos_invoicing_journal_ids/static/src/js/PaymentScreen.js',
            'l10n_pt_ao_pos_invoicing_journal_ids/static/src/js/models.js',
            'l10n_pt_ao_pos_invoicing_journal_ids/static/src/xml/paymentscreen.xml',
        ],
    },
    'application' : False,
    'auto_install': True,
}
