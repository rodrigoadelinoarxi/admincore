{
    'name': "Portugal - Certified Delivery",

    'summary': """
        Implements requirements for deliveries in Odoo with the Portuguese Certification""",
    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Warehouse',
    'version': '17.0.1.0.4',
    'license': 'OPL-1',
    'depends': ['delivery', 'l10n_pt_stock'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'auto_install': True
}
