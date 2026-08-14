{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'                 : 'Sale  - Portugal / Angola',
    'summary'              : """
        Module for common sale requirements between Portuguese and Angolan localizations""",
    'author'               : "ARXILEAD",
    'website'              : "https://www.arxi.pt",
    'category'             : 'Accounting & Finance',
    'version'              : '19.0.1.0.43',
    'license'              : 'OPL-1',
    'depends'              : [
        'l10n_pt_ao',
        'sale_report_by_country',
        'sale_management',
        'sale_journals',
        'product_matrix',
        'print_conf_copies_sales'],
    'external_dependencies': {
    },
    'data'                 : [
        'security/ir.model.access.csv',

        'data/sale_order_data.xml',
        'data/account_document_type.xml',

        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_journal_views.xml',

        'views/account_move_views.xml',
        'report/sale_order_templates.xml',
        'report/sale_order_reports.xml',

        'wizard/sale_order_cancel_views.xml',
        'wizard/sale_order_alert_wizard_views.xml',
        'wizard/account_move_reversal_view.xml',
        'wizard/sale_make_invoice_advance_views.xml',
        'wizard/mass_cancel_orders_views.xml'
    ],
    'demo'                 : [
    ],
    'assets'               : {

    },
    'auto_install'         : [
        'l10n_pt_ao',
        'sale_management'],
    'post_init_hook'       : 'post_init_hook'
}
