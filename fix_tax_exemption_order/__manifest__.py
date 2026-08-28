{
    'name': 'Fix account.tax.exemption default order',
    'version': '19.0.0.0.1',
    'author': 'ARXILEAD',
    'summary': "Fix 'account.tax.exemption' default order breaking on Odoo 19 (display_name not stored)",
    'category': 'Accounting & Finance',
    'depends': [
        'l10n_pt_ao',
    ],
    'data': [

    ],
    # l10n_pt_ao is always installed on this DB; auto_install (glue-module
    # pattern) guarantees this fix gets installed by the upgrade process
    # itself without needing to add a reverse depend to l10n_pt_ao's own
    # manifest (which would create a dependency cycle).
    'auto_install': True,
    'license': 'OPL-1',
}
