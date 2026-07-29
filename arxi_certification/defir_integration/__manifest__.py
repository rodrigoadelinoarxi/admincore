{
    'name': 'Defir Integration',
    'summary': """
        Module for Defir Integration
    """,

    'author': 'Arxi',
    'website': 'https://www.arxi.pt',
    'category': 'Accounting & Finance',
    'version': '17.0.0.1.6',
    'license': 'OPL-1',
    'depends': ['account', 'account_accountant', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'wizard/defir_integration_wizard.xml',
    ],
}
