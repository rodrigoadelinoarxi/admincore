{
    'name': 'Portugal - Payment Term Discount',
    'summary': """
        Module responsible for implementing automated Payment terms discount
    """,
    'author': "Arxi",
    'website': 'https://www.arxi.pt',
    'category': 'Accounting & Finance',
    'sequence': 150,
    'version': '17.0.0.0.8',
    'license': 'OPL-1',
    'depends': ['l10n_pt_certificate'],
    'data': [
        'views/account_move_view.xml',
        'views/product_view.xml',
        'views/account_payment_term_view.xml'
    ]
}
