{
    'name': 'Portugal - E-Invoicing (CIUS-PT)',
    'version': '17.0.0.0.9',
    'license': 'OPL-1',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'E-Invoicing, CIUS-PT standard',
    'description': """
    The semantic data model EN 16931-1 can include more data elements and definitions than required in certain 
    situations or applications. Furthermore, there is often a requirement, where some elements of the norm are not 
    optional but mandatoryCore Invoice Usage Specification (CIUS).
    This is where Core Invoice Usage Specification (CIUS) is used to further define this invoicing norm base.
    The Republic of Portugal has defined their own CIUS for e-invoices sent to the Austrian authorities. 
    This CIUS is called CIUS-PT and limits the extent of both EU invoice syntaxes UBL and CEFACT.
    """,
    'depends': ['l10n_pt_multicert', 'account_edi_ubl_cii'],
    'external_dependencies': {
        'python': ['xmltodict'],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/uom_uom_data.xml',
        'data/account_edi_data.xml',
        'data/payment_mechanism_data.xml',
        'data/cron.xml',
        'views/account_tax_views.xml',
        'views/payment_mechanism_views.xml',
        'views/account_move_views.xml',
        'views/res_config_settings_views.xml'
    ],
    'demo': [
        'demo/res_partner_demo.xml',
        'demo/product_product_demo.xml',
        'demo/account_move_demo.xml'
    ],
    'installable': True,
    'auto_install': True,
}
