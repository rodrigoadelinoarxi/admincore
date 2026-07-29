{
    'name': 'Document Print Configurations',
    'summary': """
        Module for documents print copies configuration""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Print Configuration',
    'version': '17.0.0.0.2',
    'license': 'OPL-1',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'report/print_copies_display_templates.xml',
        'report/account_move_templates.xml',
        'report/account_payment_templates.xml',
        'views/res_company.xml',
        'views/res_partner.xml',
        'views/account_move.xml',
        'views/account_payment.xml',
    ],
    'application': False,
}
