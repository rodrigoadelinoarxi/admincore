{
    'name': 'Second Discount Invoice',
    'summary': """
        Module that adds discount fields to account move line
    """,

    'author': 'Arxi',
    'website': 'https://www.arxi.pt',
    'category': 'Accounting & Finance',
    'version': '17.0.0.1.6',
    'license': 'OPL-1',
    'depends': ['display_total_discount', 'sale_second_discount'],
    'data': [
        'views/account_move_views.xml',
    ],
    'auto_install': True,
}
