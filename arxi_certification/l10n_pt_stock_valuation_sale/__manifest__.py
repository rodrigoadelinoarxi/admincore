{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Portugal - Stock Valuation Sale',
    'summary': """
        Module responsible for fixing valuation account moves account mapping from Sale Module
    """,
    'author': 'Arxi',
    'website': 'https://www.arxi.pt',
    'category': 'Hidden',
    'version': '19.0.1.0.0',
    'license': 'OPL-1',
    'depends': ['sale_stock'],
    'data': [],
    'auto_install': ['sale_stock'],
}
