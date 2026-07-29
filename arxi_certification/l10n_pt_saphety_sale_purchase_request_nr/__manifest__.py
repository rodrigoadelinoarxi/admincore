{
    'name'          : 'Portugal - Saphety Sale Order Purchase Request Number',
    'summary'       : """Adds Purchase Request Number in Sales to link with Invoices/Credit Notes.""",
    'author'        : "ARXILEAD",
    'website'       : "https://www.arxi.pt",
    'category'      : 'Accounting & Finance',
    'version'       : '17.0.0.0.5',
    'license'       : 'OPL-1',
    'depends'       : [
        'l10n_pt_saphety',
        'sale'
    ],
    'data'          : [
        'views/sale_order_views.xml',
        'report/sale_order_report.xml',
        'report/account_move_report.xml'
    ],
}
