{
    'name': 'ARXI Certification Patch - Local Signing',
    'version': '17.0.1.0.0',
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
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
