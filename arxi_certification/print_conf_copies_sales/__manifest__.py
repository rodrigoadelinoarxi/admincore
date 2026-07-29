{
    'name': 'Document Print Configurations - Sales Documents',
    'summary': """
        Module for sales documents print copies configuration""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Print Configuration',
    'version': '17.0.0.0.4',
    'license': 'OPL-1',
    'depends': ['sale', 'print_conf_copies'],
    'data': [
        'report/sale_order_templates.xml',
        'views/sale_order_views.xml',
    ],
    'auto_install': True,
    'application': False,
}
