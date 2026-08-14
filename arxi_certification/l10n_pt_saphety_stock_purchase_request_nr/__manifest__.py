{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'        : 'Portugal - Saphety Stock Purchase Request Number',
    'summary'     : """Adds Purchase Request Number in Stock Documents to link with Invoices/Credit Notes.""",
    'author'      : "ARXILEAD",
    'website'     : "https://www.arxi.pt",
    'category'    : 'Accounting & Finance',
    'version'     : '19.0.0.0.1',
    'license'     : 'OPL-1',
    'depends'     : [
        'l10n_pt_saphety_sale_purchase_request_nr',
        'l10n_pt_stock'
    ],
    'data'        : [
        'views/pt_transport_views.xml',
        'views/stock_picking_views.xml',
        'report/stock_picking_report.xml',
        'report/pt_transport_report.xml'
    ],
    'auto_install': True,
}
