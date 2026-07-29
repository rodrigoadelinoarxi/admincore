from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    # account_type = fields.Many2one('account.account.type', compute='_compute_account_type', store=True)
    #
    # @api.depends('general_account_id', 'general_account_id.user_type_id')
    # def _compute_account_type(self):
    #     for rec in self:
    #         rec.account_type = rec.general_account_id.user_type_id

    auto_account_partner_id = fields.Many2one('res.partner', compute='_compute_auto_account_partner_id', store=True)
    auto_account_partner_id_value = fields.Integer(compute='_compute_auto_account_partner_id_value', store=True)
    has_set_auto_account_partner = fields.Boolean()

    @api.depends('auto_account_partner_id')
    def _compute_auto_account_partner_id_value(self):
        for rec in self:
            rec.auto_account_partner_id_value = rec.auto_account_partner_id and rec.auto_account_partner_id.id

    def _compute_auto_account_partner_id(self):
        for rec in self:
            analytic_plan = False
            for field in rec._fields:
                if 'x_plan' in field:
                    if rec[field]:
                        analytic_plan = int(''.join(filter(str.isdigit, field)))
                        break
            rec.auto_account_partner_id = rec.with_context(
                analytic_plan_id=analytic_plan).auto_account_id and rec.with_context(
                analytic_plan_id=analytic_plan).auto_account_id.partner_id and rec.with_context(
                analytic_plan_id=analytic_plan).auto_account_id.partner_id.id or False

    def cron_sync_auto_account_partner_id(self):
        """
        This is used to fill in auto_account_partner_id something that might change due to conte
        :return:
        """
        records = self.env['account.analytic.line'].search([('has_set_auto_account_partner', '=', False)], limit=10000)
        records._compute_auto_account_partner_id()
        records.write({
            'has_set_auto_account_partner': True
        })
