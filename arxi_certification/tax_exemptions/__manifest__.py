{
    'name': "Tax Exemptions",

    'summary': """
        Adds exemption fields to taxes.""",
    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Accounting',
    'version': '17.0.1.0.1',
    'license': 'OPL-1',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_tax_views.xml',
        'views/account_tax_exemption_views.xml',
        'views/tax_exemptions_menus.xml'
    ],
}
