{
    'name': 'Portugal - Multi Payments Payment Discount',
    'summary': """Auxiliary Module to allow multi payments with financial discount""",
    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '17.0.0.0.3',
    'license': 'OPL-1',
    'depends': ['l10n_pt_multi_payment', 'l10n_pt_payment_term_discount'],
    'data': [
        'views/account_payment_views.xml',
        'wizard/account_multi_payment_register_views.xml',
    ],
    'auto_install': True,
}
