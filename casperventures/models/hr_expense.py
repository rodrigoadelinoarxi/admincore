from odoo import models


class HrExpense(models.Model):
    _inherit = "hr.expense"

    def _prepare_payments_vals(self):
        res = super(HrExpense, self)._prepare_payments_vals()
        res['date'] = self.accounting_date
        return res
