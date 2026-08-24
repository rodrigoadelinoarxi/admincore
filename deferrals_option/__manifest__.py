{
    "name": "Deferrals Options",
    "summary": """
        Create and visualize Expenses and Revenues deferrals in their respective menus and forms for Portuguese Chart of Accounts.
    """,

    "version": "19.0.0.0.1",
    'price'   : 0.00,
    'currency': 'EUR',
    "category": "Accounting & Finance",

    "author": "ARXILEAD",
    "website": "https://www.arxi.pt",
    "license": "OPL-1",

    'depends': [
        'account_asset',
        'account',
        # models/account_deferred_reports.py inherits 'account.deferred.report.handler'
        # (from account_reports) and views/account_asset_views.xml patches the
        # 'account_asset_law_id' field (from account_asset_law). Both were only
        # ever pulled in transitively (e.g. via l10n_pt_reports_arxi); installing
        # this module on its own crashed with a ParseError/model-not-found.
        # Declare them explicitly instead of relying on install order.
        'account_reports',
        'account_asset_law',
    ],

    'data': [
        'views/account_asset_views.xml',
        'views/account_move_views.xml',
        'views/account_account_views.xml',
    ],

    'installable': True,
    'images': ['static/description/banner.gif'],

}
