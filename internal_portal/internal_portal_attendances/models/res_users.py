from odoo import api, models


class Users(models.Model):
    _inherit = 'res.users'

    @api.depends('share', 'employee_id')
    def _compute_create_employee(self):
        for user in self:
            if not user.employee_id and user.has_group('internal_portal_attendances.group_internal_portal_attendances'):
                user.create_employee = True
            else:
                super(Users, user)._compute_create_employee()

    def action_create_employee(self):
        for user in self:
            user.write({
                'groups_id': [(4, self.env.ref('internal_portal_attendances.group_internal_portal_attendances').id)]
            })
        return super(Users, self).action_create_employee()
