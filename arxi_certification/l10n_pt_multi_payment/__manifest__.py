{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Portugal - Multi Payments',
    'summary': """Module that allows multi payments with write-off on a single payment""",
    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '17.0.0.0.9',
    'license': 'OPL-1',
    'depends': ['l10n_pt_certificate'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_views.xml',
        'views/account_move_views.xml',
        'wizard/account_multi_payment_register_views.xml',
    ],
}
