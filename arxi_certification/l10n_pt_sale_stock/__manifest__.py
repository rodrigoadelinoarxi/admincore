{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': True,

    'name'                 : 'Portugal - Certified Sale Stock',
    'summary'              : """
        Module for sale stock certification and compatibility""",

    'author'               : "ARXILEAD",
    'website'              : "https://www.arxi.pt",
    'category'             : 'Warehouse',
    'version'              : '1.3',
    'license'              : 'OPL-1',
    'depends'              : ['l10n_pt_stock', 'sale_stock', 'l10n_pt_ao_sale'],
    'data'                 : [

        'views/sale_order_views.xml',
    ],
    'auto_install'         : ['l10n_pt_stock', 'sale_stock'],
}
