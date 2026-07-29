{
    'name'        : 'Portugal / Angola - Certified Point of Sale Default End Consumer',
    'summary'     : """
        Module for Point of Sale Default End Consumer""",
    'author'      : "Arxi",
    'website'     : "https://www.arxi.pt",
    'category'    : 'Sales/Point Of Sale',
    'version'     : '17.0.0.0.2',
    'license'     : 'OPL-1',
    'depends'     : [
        'l10n_pt_ao_pos',
    ],
    'data'        : [
        'views/pos_config_views.xml'
    ],
    'assets'      : {
        'point_of_sale._assets_pos': [
            'l10n_pt_ao_pos_default_end_consumer/static/src/js/models/store.js',
        ],
    },
    'application' : False,
    'auto_install': False,
}
