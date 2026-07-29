import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class SaleProductHistory(models.Model):
    _name = 'sale.product.history'
    _description = 'sale.product.history'

    partner_id = fields.Many2one('res.partner', required=True)
    sale_id = fields.Many2one('sale.order', required=True)
    product_id = fields.Many2one('product.product', required=True)
    product_quant = fields.Float(required=True)
