{
    'name'          : 'Portugal - Saphety Invoice Signature with Transport Documents',
    'summary'       : """Connection between Invoices and Transport Documents for EDI.""",
    'author'        : "ARXILEAD",
    'website'       : "https://www.arxi.pt",
    'category'      : 'Accounting & Finance',
    'version'       : '17.0.0.0.2',
    'license'       : 'OPL-1',
    'depends'       : [
        'l10n_pt_saphety',
        'l10n_pt_stock'
    ],
    'data'          : [
        'views/account_move_views.xml',
    ],
}
