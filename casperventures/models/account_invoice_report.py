from odoo import models, fields
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    partner_id_value = fields.Integer(
        string='Partner ID (Technical)',
        readonly=True,
        help="Raw partner ID from the account move"
    )

    def _select(self) -> SQL:
        """Add move.partner_id to the SELECT clause"""
        # v19: _select() devolve um objeto SQL (nao string) -> compor com SQL()
        return SQL("%s, move.partner_id AS partner_id_value", super()._select())
