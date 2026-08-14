{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name'          : 'Portugal - Certified Point of Sale',
    'summary'       : """
        QR Code and ATCUD on the certified POS receipt""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Sales/Point Of Sale',
    'version': '1.2',
    'license': 'OPL-1',
    'depends': ['l10n_pt_certificate', 'l10n_pt_ao_pos'],
    'external_dependencies': {
        'python': ['qrcode'],
    },
    'data': [
        'data/pos_qr_parameters.xml',
    ],
    'assets'        : {
        'point_of_sale._assets_pos': [
            'l10n_pt_pos/static/src/js/**/*',
            'l10n_pt_pos/static/src/xml/**/*',
        ],
    },
    'auto_install' : ['l10n_pt_certificate', 'l10n_pt_ao_pos'],
    'application'   : False,
}
