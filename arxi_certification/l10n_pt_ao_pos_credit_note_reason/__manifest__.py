{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'        : 'Portugal / Angola - Certified Point of Sale Credit Note Reason',
    'summary'     : """
        Module for Point of Sale Credit Note Reason""",
    'author'      : "Arxi",
    'website'     : "https://www.arxi.pt",
    'category'    : 'Sales/Point Of Sale',
    'version'     : '17.0.0.0.6',
    'license'     : 'OPL-1',
    'depends'     : [
        'point_of_sale',
        'credit_note_reason',
    ],
    'data'        : [
    ],
    'assets'      : {
        'point_of_sale._assets_pos': [
            'l10n_pt_ao_pos_credit_note_reason/static/src/**/*',
        ],
    },
    'application' : False,
    'auto_install': True,
}
