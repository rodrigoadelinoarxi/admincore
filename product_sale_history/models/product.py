import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    categ_product_limit = fields.Boolean(related='categ_id.buy_limit_product')
    buy_limit_quant = fields.Float(string='Buying Limit', compute='_compute_buy_limit_quant', store=True, readonly=False)

    @api.depends('categ_id', 'categ_id.buy_limit_quant')
    def _compute_buy_limit_quant(self):
        for rec in self:
            if rec.categ_id:
                rec.buy_limit_quant = rec.categ_id.buy_limit_quant
            else:
                rec.buy_limit_quant = 0.0
