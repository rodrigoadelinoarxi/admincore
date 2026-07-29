from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    planning_slot_id = fields.Many2one('planning.slot', string='Planning Slot')
