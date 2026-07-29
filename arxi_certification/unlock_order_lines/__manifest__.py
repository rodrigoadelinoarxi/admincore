{
    'name': 'Unlock Order_lines',
    'summary': """
        Module unlocks all fields from order lines that dont go on SAFT""",
    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '17.0.1.0.02',
    'license': 'OPL-1',
    'depends': ['l10n_pt_ao_sale'],
    'external_dependencies': {
    },
    'data': [
        'views/sale_order_views.xml',
    ],
    'demo': [
    ],
    'application': True,
}
