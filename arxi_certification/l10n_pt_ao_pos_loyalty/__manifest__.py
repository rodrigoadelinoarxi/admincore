{
    # Desativado temporariamente na migracao 17->19 (2026-07-30): o binario
    # PyArmor deste modulo (pyarmor_runtime_009591/pyarmor_runtime.so) foi
    # compilado para uma versao de Python mais antiga e da erro de simbolo
    # indefinido (_PyFloat_Pack8) no Python 3.12 do container Odoo 19 —
    # precisa de ser recompilado/re-protegido para Python 3.12 pela Arxi antes
    # de poder ser reativado. Nao e um problema de dados da migracao.
    'installable': False,

    'name': 'Portugal / Angola - Certified Point of Sale and Loyalty Program',
    'summary': """
        Module for POS certification and Loyalty Program""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Sales/Point Of Sale',
    'version': '19.0.0.0.2',
    'license': 'OPL-1',
    'depends': [
        'l10n_pt_ao_pos',
        'pos_loyalty'
    ],
    'data': [
        'views/pos_loyalty_views.xml',
        'views/product_views.xml',
        # 'views/res_partner_views.xml'
    ],
    'assets': {
        'point_of_sale.assets': [
            'l10n_pt_ao_pos_loyalty/static/src/js/**/*',
        ],
        'web.assets_qweb': [],
    },
    'auto_install': False,
    'application': False,
}
