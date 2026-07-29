from odoo import api, fields, models, _


def name_boolean_group(id):
    return 'in_group_' + str(id)


class Users(models.Model):
    _inherit = 'res.users'

    create_employee = fields.Boolean(string='Create Employee', compute='_compute_create_employee', store=True)

    @api.depends('share', 'employee_id')
    def _compute_create_employee(self):
        for user in self:
            user.create_employee = not user.employee_id and not user.share

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super(Users, self).fields_get(allfields, attributes=attributes)
        # add reified groups fields

        for app, kind, gs, category_name in self.env['res.groups'].sudo().get_portal_groups_to_view():
            for g in gs:
                field_name = name_boolean_group(g.id)
                if allfields and field_name not in allfields:
                    continue
                res[field_name] = {
                    'type'      : 'boolean',
                    'string'    : g.name,
                    'help'      : g.comment,
                    'exportable': False,
                    'selectable': False,
                }

        return res
