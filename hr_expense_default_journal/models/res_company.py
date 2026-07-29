from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    expense_default_journal_id = fields.Many2one(
        'account.journal',
        string='Expense Default Journal',
        domain=[('type', '=', 'purchase')]
    )
