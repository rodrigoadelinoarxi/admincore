{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Document Print Configurations Certificate',
    'summary': """
        Module for documents print copies configuration for certificate reports""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Print Configuration PT',
    'version': '17.0.0.0.5',
    'license': 'OPL-1',
    'depends': ['l10n_pt_stock', 'print_conf_copies'],
    'data': [
        'report/transport_document_report.xml',
        'report/delivery_slip_report.xml',
        'report/picking_operations.xml',
        'views/pt_transport_views.xml',
        'views/stock_picking_views.xml',

    ],
    'auto_install': True,
    'application': False,
}
