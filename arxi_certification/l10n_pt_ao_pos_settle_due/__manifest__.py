{
    'name': 'Portugal / Angola - Certified Point of Sale Settle Due',
    'summary': """
        Module for POS certification with Settle Due Option""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Sales/Point Of Sale',
    'version': '19.0.0.0.1',
    'license': 'OPL-1',
    'depends': [
        'l10n_pt_ao_pos',
        'pos_settle_due',
    ],
    'data': [
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_pt_ao_pos_settle_due/static/src/js/**/*',
        ],
    },
    'auto_install': True,
    'application': False,
}
