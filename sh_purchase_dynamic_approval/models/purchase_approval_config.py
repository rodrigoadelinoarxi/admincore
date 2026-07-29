# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseApprovalConfig(models.Model):
    _name = 'sh.purchase.approval.config'
    _description = 'Purchase Approval Configuration'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char()
    min_amount = fields.Float(string="Minimum Amount", required=True)
    company_ids = fields.Many2many(
        'res.company', string="Allowed Companies", default=lambda self: self.env.company)
    purchase_approval_line_ids = fields.One2many(
        'sh.purchase.approval.line', 'purchase_approval_config_id')
