# -*- coding: utf-8 -*-
{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': True,

    'name': "Consignment Invoices",
    'license': 'OPL-1',
    'summary': """Consignment Invoice Menu""",
    'description': """
        Added Menu Item and Action to view and create Consignment Invoices.
    """,

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",

    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['l10n_pt_ao_sale'],

    # always loaded
    'data': [
        'views/sale_order_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'post_init_hook'       : 'post_init_hook'
}
