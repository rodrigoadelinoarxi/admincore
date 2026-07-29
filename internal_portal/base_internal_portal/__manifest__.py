# noinspection PyStatementEffect
{
    'name': "Internal Portal Base",
    'summary': """Internal Portal Base""",
    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'license': 'OPL-1',
    'category': 'Uncategorized',
    'version': '17.0.0.0.0',
    'depends': [
        'hr',
        'portal',
    ],
    'data': [
        # Security
        'security/groups.xml',
        # Backend views
        'views/res_users_views.xml',
    ],
    'assets': {
    },
}
