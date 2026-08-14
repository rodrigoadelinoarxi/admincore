{
    "name": "Deferrals Options",
    "summary": """
        Create and visualize Expenses and Revenues deferrals in their respective menus and forms for Portuguese Chart of Accounts.
    """,

    "version": "19.0.0.0.12",
    'price'   : 0.00,
    'currency': 'EUR',
    "category": "Accounting & Finance",

    "author": "ARXILEAD",
    "website": "https://www.arxi.pt",
    "license": "OPL-1",

    'depends': [
        'account_asset',
        'account',
    ],

    'data': [
        'views/account_asset_views.xml',
        'views/account_move_views.xml',
        'views/account_account_views.xml',
    ],

    'installable': True,
    'images': ['static/description/banner.gif'],

}
