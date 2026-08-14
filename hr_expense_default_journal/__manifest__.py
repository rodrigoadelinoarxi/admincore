{
    'name': "Expense Default Journal",

    'summary': """Adds a default journal for expense moves.""",
    'author': "Arxi",
    'website': "http://www.arxi.pt",
    'category': 'Human Resources',
    'version': '19.0.0.0.1',
    'license': 'OPL-1',
    'depends': ['hr_expense'],
    'data': [
        'views/res_config_settings_views.xml'
    ],
    "auto_install": False,
}
