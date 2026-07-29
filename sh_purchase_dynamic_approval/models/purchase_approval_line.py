from odoo import api, fields, models


class PurchaseApprovalLine(models.Model):
    _name = 'sh.purchase.approval.line'
    _description = 'Dynamic Purchase Approval'

    # from_amount = fields.Float(required=True)
    # to_amount = fields.Float(required=True)
    level = fields.Integer(required=True)
    approve_by = fields.Selection(
        [('group', 'Group'), ('user', 'User')], string="Approve Process By", default="user", required=True
    )
    user_ids = fields.Many2many('res.users', string="Users")
    group_ids = fields.Many2many('res.groups', string="Groups")
    purchase_approval_config_id = fields.Many2one('sh.purchase.approval.config')

    _sql_constraints = [
        ('unique_level', 'UNIQUE(level, purchase_approval_config_id)', 'You should have only one line per level'),
    ]
