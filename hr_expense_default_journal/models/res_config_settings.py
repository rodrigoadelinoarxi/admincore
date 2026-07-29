from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    expense_default_journal_id = fields.Many2one(
        string='Expense Default Journal',
        related='company_id.expense_default_journal_id',
        readonly=False
    )

