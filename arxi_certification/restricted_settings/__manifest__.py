{
    'name': 'Restricted Settings',
    'summary': """Non-superuser admins change reports or install apps""",
    'version': '17.0.0.0.1',
    'author': 'Arxi',
    'website' : 'https://www.arxi.pt',
    'category': 'Extra Tools',
    'license': 'OPL-1',
    'depends': ['base_install_request'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml'
    ],
}
