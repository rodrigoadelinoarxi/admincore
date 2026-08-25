from odoo import models, fields
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    partner_id_value = fields.Integer(
        string='Partner ID (Technical)',
        readonly=True,
        help="Raw partner ID from the account move"
    )

    def _select(self):
        # Odoo 19: _select() devolve um objeto SQL (nao uma string), para
        # compor queries em segurança — nao se pode concatenar com "+"
        # (TypeError: unsupported operand type(s) for +: 'SQL' and 'str').
        # Compor sempre via SQL(), como o proprio core faz.
        return SQL('%s, move.partner_id AS partner_id_value', super()._select())
