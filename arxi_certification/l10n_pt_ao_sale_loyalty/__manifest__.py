# -*- coding: utf-8 -*-
{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'        : "Sale Loyalty - Portugal / Angola",
    'license'     : 'OPL-1',
    'summary'     : """Hide Shipping button in Certified Sale Order""",
    'description' : """
        Hide Shipping button in Certified Sale Order
    """,

    'author'      : "Arxi",
    'website'     : "https://www.arxi.pt",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category'    : 'Uncategorized',
    'version'     : '19.0.1.0.2',

    # any module necessary for this one to work correctly
    'depends'     : ['sale_loyalty', 'l10n_pt_ao_sale'],

    # always loaded
    'data'        : [
        'views/sale_order_inherit.xml',
    ],

    'auto_install': True,
}
