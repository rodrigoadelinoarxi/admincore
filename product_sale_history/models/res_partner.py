import logging
from odoo import models, fields, api, _, Command
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    products_limit_ids = fields.One2many('res.partner.limit', 'partner_id')


class ResPartnerLimit(models.Model):
    _name = 'res.partner.limit'
    _description = "Model to save the quantity of a product that can be set on purchase"

    partner_id = fields.Many2one('res.partner', 'Partner')
    product_id = fields.Many2one('product.product', 'Product')
    quant = fields.Float('Limit Quantity')
