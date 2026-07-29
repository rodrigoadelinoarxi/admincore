{
    'name': 'Document Print Configurations Certificate',
    'summary': """
        Module for documents print copies configuration for certificate reports""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Print Configuration PT',
    'version': '17.0.0.0.5',
    'license': 'OPL-1',
    'depends': ['l10n_pt_stock', 'print_conf_copies'],
    'data': [
        'report/transport_document_report.xml',
        'report/delivery_slip_report.xml',
        'report/picking_operations.xml',
        'views/pt_transport_views.xml',
        'views/stock_picking_views.xml',

    ],
    'auto_install': True,
    'application': False,
}
