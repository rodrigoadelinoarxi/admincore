{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

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
