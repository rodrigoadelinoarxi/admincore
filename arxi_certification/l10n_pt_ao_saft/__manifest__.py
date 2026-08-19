{
    # CORRIGIDO 2026-08-19: o binario PyArmor deste modulo JA foi recompilado
    # pela Arxi para Python 3.12 (commit 6e30f65, 2026-08-13) - a versao
    # entregue pela Arxi nao declara 'installable' (default True). O merge
    # 41a25a7 (2026-08-14) resolveu incorretamente o conflito deste ficheiro
    # a favor da versao local antiga ('installable': False, de 80f81ed,
    # 2026-07-30), ao contrario do que o resto do merge fez (favorecer a
    # versao da Arxi) - bloqueava desnecessariamente todo o cluster
    # l10n_pt_certificate/l10n_pt_sale/l10n_pt_stock/casperventures.
    'name': 'SAF-T',
    'summary': """
        Module for SAF-T""",

    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '1.0',
    'license': 'OPL-1',
    'depends': ['l10n_pt_ao'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/saft_import_wizard_views.xml',
    ],
    'assets': {
    },
    'auto_install': ['l10n_pt_ao'],
}
