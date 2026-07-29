from odoo import fields, models


class ApprovalInfo(models.Model):
    _inherit = 'sh.approval.info'

    purchase_order_id = fields.Many2one('purchase.order')
    additional_info = fields.Char(string="Additional Information", readonly=True)
