# -*- coding: utf-8 -*-
{
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
    'version'     : '17.0.1.0.2',

    # any module necessary for this one to work correctly
    'depends'     : ['sale_loyalty', 'l10n_pt_ao_sale'],

    # always loaded
    'data'        : [
        'views/sale_order_inherit.xml',
    ],

    'auto_install': True,
}
