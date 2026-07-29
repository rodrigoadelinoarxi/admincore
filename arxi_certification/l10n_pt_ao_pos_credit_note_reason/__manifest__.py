{
    'name'        : 'Portugal / Angola - Certified Point of Sale Credit Note Reason',
    'summary'     : """
        Module for Point of Sale Credit Note Reason""",
    'author'      : "Arxi",
    'website'     : "https://www.arxi.pt",
    'category'    : 'Sales/Point Of Sale',
    'version'     : '17.0.0.0.6',
    'license'     : 'OPL-1',
    'depends'     : [
        'point_of_sale',
        'credit_note_reason',
    ],
    'data'        : [
    ],
    'assets'      : {
        'point_of_sale._assets_pos': [
            'l10n_pt_ao_pos_credit_note_reason/static/src/**/*',
        ],
    },
    'application' : False,
    'auto_install': True,
}
