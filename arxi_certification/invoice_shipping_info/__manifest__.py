{
    'name'    : 'Invoice Shipping Info',
    'summary' : """Adds shipping fields on invoices""",
    'author'  : "ARXILEAD",
    'website' : "https://www.arxi.pt",
    'category': 'Invoicing',
    'version' : '17.0.1.0.10',
    'license' : 'OPL-1',
    'depends' : ['account'],
    'data'    : [
        'views/account_move_views.xml',
        'report/account_move_templates.xml'
    ],
}
