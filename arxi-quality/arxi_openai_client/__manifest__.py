{
    'name': 'Arxi OpenAI Client',
    'version': '17.0.1.0.0',
    'category': 'Technical',
    'summary': 'OpenAI API client wrapper for Odoo modules',
    'author': 'Arxi',
    'website': 'https://www.arxi.pt',
    'depends': ['base'],
    'data': [
        'data/ir_config_parameter.xml',
    ],
    # CORRIGIDO 2026-08-19: o binario PyArmor deste modulo JA foi recompilado
    # pela Arxi para Python 3.12 (commit 6e30f65, 2026-08-13, 'installable':
    # True explicito). O merge 41a25a7 (2026-08-14) resolveu incorretamente
    # o conflito deste ficheiro a favor da versao local antiga ('installable':
    # False, de 80f81ed, 2026-07-30).
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
