{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Portugal - Multi Payments Payment Discount',
    'summary': """Auxiliary Module to allow multi payments with financial discount""",
    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '19.0.0.0.3',
    'license': 'OPL-1',
    'depends': ['l10n_pt_multi_payment', 'l10n_pt_payment_term_discount'],
    'data': [
        'views/account_payment_views.xml',
        'wizard/account_multi_payment_register_views.xml',
    ],
    'auto_install': True,
}
