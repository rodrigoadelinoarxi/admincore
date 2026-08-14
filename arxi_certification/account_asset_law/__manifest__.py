{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Assets Management - Law',
    'summary': 'Adds legislation fields to create asset models',
    'category': 'Accounting/Accounting',
    'depends': ['account_asset'],
    'version': '19.0.1.0.5',
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'data/account_asset_law_category_data.xml',
        'data/account_asset_law_data.xml',
        'views/account_asset_law_views.xml',
        'views/account_asset_law_category_views.xml',
        'views/account_asset_views.xml',
        'views/res_company_views.xml',
        'views/company_activity_index_views.xml',
        'views/account_asset_law_menus.xml',
    ],
}
