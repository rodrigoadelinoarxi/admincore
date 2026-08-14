{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Subscriptions - Portugal / Angola',
    'summary': """
        Module for common subscription requirements between Portuguese and Angolan localizations""",
    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Sales/Subscriptions',
    'version': '19.0.0.0.4',
    'license': 'OPL-1',
    'depends': ['l10n_pt_ao_sale', 'sale_subscription'],
    'external_dependencies' : {
    },
    'data': [
        'data/sale_order_type.xml',
        'views/sale_order_journal_views.xml',
        'views/sale_subscription_views.xml',
        'views/sale_order_views.xml',
        'report/sale_order_templates.xml'
    ],
    'demo': [
    ],
    'auto_install': True,
    'post_init_hook': 'post_init_hook'
}
