{
    'name': 'Portugal - Multi Payments',
    'summary': """Module that allows multi payments with write-off on a single payment""",
    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '17.0.0.0.9',
    'license': 'OPL-1',
    'depends': ['l10n_pt_certificate'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_views.xml',
        'views/account_move_views.xml',
        'wizard/account_multi_payment_register_views.xml',
    ],
}
