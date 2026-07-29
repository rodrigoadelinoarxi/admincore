{
    'name': 'Accounting - Credit Note Specific Account',
    'summary': """
        This modules add the option to choose an account when creating a refund.
        That account will be used in the product lines.
    """,
    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'depends': ['l10n_pt_ao'],
    'data': [
        'wizard/account_move_reverse_views.xml'
    ],
    'auto_install'         : True,
}
