{
    # CORRIGIDO 2026-08-19: o binario PyArmor deste modulo JA foi recompilado
    # pela Arxi para Python 3.12 (commit 6e30f65, 2026-08-13) - a versao
    # entregue pela Arxi nao declara 'installable' (default True). O merge
    # 41a25a7 (2026-08-14) resolveu incorretamente o conflito deste ficheiro
    # a favor da versao local antiga ('installable': False, de 80f81ed,
    # 2026-07-30), ao contrario do que o resto do merge fez (favorecer a
    # versao da Arxi) - bloqueava desnecessariamente todo o cluster
    # l10n_pt_certificate/l10n_pt_sale/l10n_pt_stock/casperventures.
    'name': 'Subscriptions - Portugal / Angola',
    'summary': """
        Module for common subscription requirements between Portuguese and Angolan localizations""",
    'author': "ARXILEAD",
    'website': "https://www.arxi.pt",
    'category': 'Sales/Subscriptions',
    'version': '1.2',
    'license': 'OPL-1',
    'depends': ['l10n_pt_ao_sale', 'sale_subscription'],
    'external_dependencies' : {
    },
    'data': [
        'data/sale_order_type.xml',
        'views/sale_order_journal_views.xml',
        'views/sale_subscription_views.xml',
        'views/sale_order_views.xml',
        'report/sale_order_templates.xml'
    ],
    'demo': [
    ],
    'auto_install': True,
    'post_init_hook': 'post_init_hook'
}
