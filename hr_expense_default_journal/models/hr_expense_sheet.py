from odoo import api, fields, models


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    @api.model
    def _default_journal_id(self):
        if self.env.company.expense_default_journal_id:
            return self.env.company.expense_default_journal_id.id
        else:
            return super(HrExpenseSheet, self)._default_journal_id()

    journal_id = fields.Many2one(default=_default_journal_id)
