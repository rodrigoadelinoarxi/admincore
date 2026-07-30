# -*- coding: utf-8 -*-
{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': "l10n_pt_ao_so_user_id_editable",
    'license': 'OPL-1',
    'summary': """user_id id editable""",
    'description': """
        After creating sale order,Salesperso in  more info tab is uneditable. with this module, field
        will be aditable ever
    """,

    'author': "Arxi",
    'website': "https://www.arxi.pt",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'views/sale_order_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
