{
    'name'       : 'Admin Expiration Panel',
    'summary'    : 'Show the Expiration Panel only to Admin users',

    'author'     : 'Arxi',
    'website'    : 'http://www.arxi.pt',
    'category'   : 'Product',

    'version'    : '17.0.0.0.5',
    'license'    : 'OPL-1',

    'price': 0.00,
    'currency': 'EUR',

    'depends'    : ['web_enterprise'],

    'data'       : [
    ],

    'images'     : [
        'static/description/banner.png',
    ],

    'assets': {
        'web.assets_backend': [
            'admin_expiration_panel/static/src/js/*.js',
            'admin_expiration_panel/static/src/js/*.xml',
        ],
    },

    'installable': True,
}
