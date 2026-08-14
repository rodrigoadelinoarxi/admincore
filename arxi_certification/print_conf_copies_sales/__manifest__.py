{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Document Print Configurations - Sales Documents',
    'summary': """
        Module for sales documents print copies configuration""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Print Configuration',
    'version': '19.0.0.0.4',
    'license': 'OPL-1',
    'depends': ['sale', 'print_conf_copies'],
    'data': [
        'report/sale_order_templates.xml',
        'views/sale_order_views.xml',
    ],
    'auto_install': True,
    'application': False,
}
