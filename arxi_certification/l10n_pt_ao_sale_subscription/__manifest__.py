{
    # CORRIGIDO 2026-08-19: o binario PyArmor deste modulo JA foi recompilado
    # pela Arxi para Python 3.12 (commit 6e30f65, 2026-08-13) - a versao
    # entregue pela Arxi nao declara 'installable' (default True). O merge
    # 41a25a7 (2026-08-14) resolveu incorretamente o conflito deste ficheiro
    # a favor da versao local antiga ('installable': False, de 80f81ed,
    # 2026-07-30), ao contrario do que o resto do merge fez (favorecer a
    # versao da Arxi) - bloqueava desnecessariamente todo o cluster
    # l10n_pt_certificate/l10n_pt_sale/l10n_pt_stock/casperventures.
    #
    # RE-DESATIVADO 2026-08-19 12:24 (bug DIFERENTE do PyArmor, so este
    # modulo): o binario carrega e importa bem agora, mas o proprio codigo
    # (protegido, nao editavel) tem um bug real de v17->v19: o override de
    # SaleOrderLine._compute_discount() (models/sale_order.py, cluster
    # l10n_pt_ao_sale_subscription do repo de referencia
    # skills/repo/fontes/custom-addons/l10n_pt_ao/l10n_pt_ao_sale_subscription/
    # models/sale_order.py:206) declara
    # @api.depends('product_id', 'product_uom', 'product_uom_qty') -
    # 'product_uom' e' o nome do campo em v17; o Odoo 19 core renomeou para
    # 'product_uom_id' (confirmado em odoo/addons/sale/models/sale_order_line.py
    # do proprio odoo:19, linha ~132). Rebentava
    # "ValueError: Wrong @depends on '_compute_discount' ... Dependency field
    # 'product_uom' not found in model sale.order.line" ao carregar o registry
    # (run 17_to_19_20260819_115624, iteracao 8). Como o ficheiro esta
    # protegido por PyArmor, nao ha como corrigir o decorator @api.depends
    # sem um novo build da Arxi (mesma familia do bloqueio pendente da
    # certificacao fiscal, ver memory/project_migracao_admincore_17_19.md).
    # Nenhum outro modulo do repo depende de l10n_pt_ao_sale_subscription
    # (grep confirmado) - desativar so este nao afeta o resto do cluster
    # (l10n_pt_certificate/l10n_pt_sale/l10n_pt_stock/casperventures
    # continuam 'installable': True).
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
    'installable': False,
    'auto_install': True,
    'post_init_hook': 'post_init_hook'
}
