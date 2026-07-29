from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    # foi removido ,check_company=True do analytic_group_id devido a ter sido removido o campo company_id em account.analytic.plan de base v17.
    analytic_group_id = fields.Many2one('account.analytic.plan')

    @api.model
    def _create_analytic_account_from_values(self, values):
        res = super(Project, self)._create_analytic_account_from_values(values)
        if values.get('analytic_group_id'):
            res.write({'plan_id': values.get('analytic_group_id')})
        return res

    def _create_analytic_account(self):
        super(Project, self)._create_analytic_account()
        for project in self:
            project.analytic_account_id.write({
                'plan_id': project.analytic_group_id.id
            })

    def write(self, vals):
        res = super(Project, self).write(vals)
        if 'analytic_group_id' in vals and self.analytic_account_id:
            self.analytic_account_id.write({
                'plan_id': vals.get('analytic_group_id')
            })
        return res
