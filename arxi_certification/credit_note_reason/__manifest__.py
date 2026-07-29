{
    'name': 'Accounting - Credit Note Reason',
    'summary': """
        Module responsible for adding (Many2one) reasons for credit note creation from the invoice
    """,
    'author': "Arxi",
    'website': "https://www.arxi.pt",
    'category': 'Accounting & Finance',
    'version': '17.0.1.0.3',
    'license': 'OPL-1',
    'depends': ['l10n_pt_ao'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_refund_reason.xml',
        'wizard/account_move_reversal_views.xml'
    ]
}
