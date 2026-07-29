{
    'name'          : 'Portugal - Saphety Invoice Signature with Buyer Code in Products',
    'summary'       : """Adds Buyer Code in Products to link with Invoices/Credit Notes.""",
    'author'        : "ARXILEAD",
    'website'       : "https://www.arxi.pt",
    'category'      : 'Accounting & Finance',
    'version'       : '17.0.0.0.3',
    'license'       : 'OPL-1',
    'depends'       : [
        'l10n_pt_saphety'
    ],
    'data'          : [

        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
    ],
}
