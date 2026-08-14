{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Portugal - E-Invoicing (CIUS-PT) - Feature Partner Filter',
    'version': '19.0.0.0.3',
    'license': 'OPL-1',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'E-Invoicing, CIUS-PT standard',
    'description': """""",
    'depends': ['account_edi'],
    'data': [
        'views/res_partner_views.xml'
    ],
}
