from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    partner_id_value = fields.Integer(
        string='Partner ID (Technical)',
        readonly=True,
        help="Raw partner ID from the account move"
    )

    def _select(self):
        """Add move.partner_id to the SELECT clause"""
        return super()._select() + ", move.partner_id AS partner_id_value"
