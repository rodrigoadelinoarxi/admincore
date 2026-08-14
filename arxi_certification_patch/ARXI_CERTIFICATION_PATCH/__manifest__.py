{
    'name': 'ARXI Certification Patch - Local Signing',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'Local certificate signing for Portuguese invoices',
    'description': '''
        This module patches the l10n_pt_certificate module to enable local signing
        of documents without remote hash retrieval, while maintaining instance validation.

        Features:
        - Local RSA signing using private key
        - Maintains contract instance validation
        - Compatible with ARXI certification requirements
        - Overrides account_mixin, account_move, and at_webservice_mixin methods
    ''',
    'author': 'ARXI',
    'website': 'https://arxi.pt',
    'depends': ['l10n_pt_certificate'],
    'data': [],
    # Desativado temporariamente na migracao 17->19 (2026-07-30): depende de
    # l10n_pt_certificate, que por sua vez esta desativado por ter o mesmo
    # problema de binario PyArmor incompativel com Python 3.12 (ver nota em
    # arxi_certification/l10n_pt_certificate/__manifest__.py).
    'installable': False,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
