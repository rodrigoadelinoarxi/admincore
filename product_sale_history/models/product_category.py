import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ProductCategory(models.Model):
    _inherit = 'product.category'

    auto_validate_and_email = fields.Boolean(string='Automatic Validate Picking And Send Email')
    email_template_id = fields.Many2one('mail.template', string='Automatic Email on Picking')
    buy_limit_category = fields.Boolean(string='Buying Limit for Category')
    buy_limit_quant = fields.Float(string='Buying Limit for Category Quant', default=0.0)
    buy_limit_product = fields.Boolean(string='Buying Limit for Product')
