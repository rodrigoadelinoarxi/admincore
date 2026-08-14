{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': "Account Cancel With Reason",

    'summary': """
        Allows canceling accounting entries and storing a cancelling reason.""",
    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Accounting',
    'version': '19.0.1.0.2',
    'license': 'OPL-1',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/cancel_invoice_wizard_views.xml',
        'views/account_payment_views.xml',
        'views/account_move_views.xml',
        'report/account_move_templates.xml',
        'report/account_payment_templates.xml'
    ],
    'auto_install': True,
    'application': False,
}
