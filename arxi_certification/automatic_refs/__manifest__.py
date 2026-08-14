{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'    : "Autoincrement References",

    'summary' : """Creates Auto incremented references for partners and products""",
    'license' : 'OPL-1',
    'author'  : "ARXILEAD",
    'website' : "https://www.arxi.pt",
    'category': 'Tools',
    'version' : '19.0.0.0.7',
    'depends' : ['account'],
    'data'    : [
        'views/res_config_settings_views.xml',
        'views/res_partner_view.xml',
        'data/config_param.xml'
    ],
}
