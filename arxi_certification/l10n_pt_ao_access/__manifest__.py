{
    'name'    : "Certification Accesses",
    'summary' : """Limit access to Certification configurations""",
    'license' : 'OPL-1',
    'author'  : "ARXILEAD",
    'website' : "https://www.arxi.pt",
    'category': 'Tools',
    'version' : '17.0.0.0.7',
    'depends' : ['base', 'l10n_pt_ao'],
    'data'    : [
        'security/ir.model.access.csv',
        'security/access_apps_security.xml',
        'wizard/installation_warning_views.xml',
    ],
    'auto_install': True,
}
