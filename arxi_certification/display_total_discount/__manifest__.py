{
    'name': 'Display Total Discount',
    'summary': """
        Module responsible for implementing Global Discount in the sales
    """,

    'author': 'Arxi',
    'website': 'https://www.arxi.pt',
    'category': 'Accounting & Finance',
    'version': '17.0.0.1.3',
    'license': 'OPL-1',
    'depends': ['delivery', 'sale', 'account'],
    'data': [
        'data/global_discount_data.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'report/sale_order_templates.xml',
    ],
}
