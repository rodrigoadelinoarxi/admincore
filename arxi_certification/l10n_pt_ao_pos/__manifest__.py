{
    'name': 'Portugal / Angola - Certified Point of Sale',
    'summary': """
        Module for POS certification and exporting SAF-T""",

    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'category': 'Sales/Point Of Sale',
    'version': '17.0.0.0.18',
    'license': 'OPL-1',
    'depends': [
        'l10n_pt_ao',
        'point_of_sale',
        'pos_hr'
    ],
    'data': [
        'report/account_move_templates.xml',
        'views/res_config_settings_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_pt_ao_pos/static/src/js/**/*',
            'l10n_pt_ao_pos/static/src/js/Screens/TicketScreen/ControlButtons/InvoiceButton.js',
            'l10n_pt_ao_pos/static/src/xml/**/*',
            'l10n_pt_ao_pos/static/src/css/**/*',
        ],
    },
    'application': False,
}
