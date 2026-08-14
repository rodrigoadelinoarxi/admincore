{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Portugal - Certified Sales',
    'summary': """
        Module for sales certification and exporting SAF-T""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'sequence': 151,
    'version': '1.17',
    'license': 'OPL-1',
    'depends': ['l10n_pt_certificate', 'l10n_pt_ao_sale', 'event_sale'],
    'data': [
        'report/sale_order_templates.xml',
        'views/sale_order_journal_views.xml',
        'views/sale_order_views.xml'
    ],
    'demo': [
        'demo/account_series.xml',
    ],
    'auto_install': True,
    'application': False,
    'post_init_hook': 'post_init_hook'
}
