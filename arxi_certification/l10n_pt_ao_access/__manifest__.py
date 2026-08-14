{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'    : "Certification Accesses",
    'summary' : """Limit access to Certification configurations""",
    'license' : 'OPL-1',
    'author'  : "ARXILEAD",
    'website' : "https://www.arxi.pt",
    'category': 'Tools',
    'version' : '1.0',
    'depends' : ['base', 'l10n_pt_ao'],
    'data'    : [
        'security/ir.model.access.csv',
        'security/access_apps_security.xml',
        'wizard/installation_warning_views.xml',
    ],
    'auto_install' : True,
}
