{
    'name': 'ARXI Certification Patch - Local Signing',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Localizations/EDI',
    'summary': 'Local certificate signing for Portuguese invoices',
    'description': '''
        This module patches l10n_pt_certificate/l10n_pt_ao to enable local signing
        of documents without remote hash/certificate retrieval, while maintaining
        instance validation.

        v19 note: Etapa 2.6 of the v19 migration moved certification hashing to a
        remote-only pipeline (`_get_remote_hash`/`_get_remote_certificate`, calling
        the Arxi central server); this patch overrides those two methods (not
        `_get_private_key`, which no longer exists) to sign/authenticate locally
        instead. AO webservice certificate not embedded — falls back to remote for AO.

        Features:
        - Local RSA signing using an embedded private key
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
