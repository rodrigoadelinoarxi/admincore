{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'        : 'Portugal / Angola - Certified Point of Sale Select Invoicing Journal',
    'summary'     : """
        Module for POS Select Invoicing Journal""",

    'author'      : "Arxi",
    'website'     : "https://www.arxi.pt",
    'category'    : 'Sales/Point Of Sale',
    'version'     : '19.0.0.0.2',
    'license'     : 'OPL-1',
    'depends'     : [
        'l10n_pt_ao_pos',
    ],
    'data'        : [
        'views/res_config_settings_views.xml'
    ],
    'assets'      : {
        'point_of_sale._assets_pos': [
            'l10n_pt_ao_pos_invoicing_journal_ids/static/src/js/PaymentScreen.js',
            'l10n_pt_ao_pos_invoicing_journal_ids/static/src/js/models.js',
            'l10n_pt_ao_pos_invoicing_journal_ids/static/src/xml/paymentscreen.xml',
        ],
    },
    'application' : False,
    'auto_install': True,
}
