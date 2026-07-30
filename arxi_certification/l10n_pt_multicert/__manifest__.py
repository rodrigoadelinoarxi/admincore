{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'          : 'Portugal - Invoice Signature',
    'summary'       : """Signs invoices with Multicert.""",
    'author'        : "ARXILEAD",
    'website'       : "https://www.arxi.pt",
    'category'      : 'Accounting & Finance',
    'version'       : '17.0.0.0.2',
    'license'       : 'OPL-1',
    'depends'       : [
        'account_edi',
        'l10n_pt_certificate'
    ],
    'data'          : [
        'data/account_edi_data.xml',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml'
    ],
    'demo': [
        'demo/res_company_demo.xml',
    ],
    'post_init_hook': 'post_init',
}
