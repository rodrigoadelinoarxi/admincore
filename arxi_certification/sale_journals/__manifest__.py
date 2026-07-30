{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Multiple Sale Journals',
    'summary': """
        Configure different sale journals and document types""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Sales',
    'version': '17.0.1.0.17',
    'license': 'OPL-1',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'security/res_groups.xml',
        'data/sale_order_type.xml',
        'report/sale_order_templates.xml',
        'views/sale_order_type_views.xml',
        'views/sale_order_journal_views.xml',
        'views/sale_order_views.xml',
        'views/sale_journals_menus.xml',
        'views/res_config_settings_views.xml',
    ],
    'auto_install': False,
    'application': False,
    'post_init_hook': 'post_init_hook'
}
