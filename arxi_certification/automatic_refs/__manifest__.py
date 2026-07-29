{
    'name'    : "Autoincrement References",

    'summary' : """Creates Auto incremented references for partners and products""",
    'license' : 'OPL-1',
    'author'  : "ARXILEAD",
    'website' : "https://www.arxi.pt",
    'category': 'Tools',
    'version' : '17.0.0.0.7',
    'depends' : ['account'],
    'data'    : [
        'views/res_config_settings_views.xml',
        'views/res_partner_view.xml',
        'data/config_param.xml'
    ],
}
