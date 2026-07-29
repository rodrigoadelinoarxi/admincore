{
    'name'        : 'Portugal / Angola - Certified Point of Sale Select Document Type',
    'summary'     : """
        Module for POS Select Document Type""",

    'author'      : "Arxi",
    'website'     : "https://www.arxi.pt",
    'category'    : 'Sales/Point Of Sale',
    'version'     : '17.0.0.0.1',
    'license'     : 'OPL-1',
    'depends'     : [
        'l10n_pt_ao_pos',
    ],
    'data'        : [
    ],
    'assets'      : {
        'point_of_sale._assets_pos': [
            'l10n_pt_ao_pos_document_type/static/src/js/PaymentScreen.js',
            'l10n_pt_ao_pos_document_type/static/src/js/models.js',
            'l10n_pt_ao_pos_document_type/static/src/xml/paymentscreen.xml',
        ],
    },
    'application' : False,
    'auto_install': True,
}
