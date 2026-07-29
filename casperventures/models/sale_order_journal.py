from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderJournal(models.Model):
    _inherit = 'sale.order.journal'

    default_invoice_journal = fields.Many2one('account.journal')
