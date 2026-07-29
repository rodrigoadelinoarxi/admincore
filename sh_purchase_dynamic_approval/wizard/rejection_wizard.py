from odoo import fields, models, _


class RejectionReasonWizard(models.TransientModel):
    _name = 'sh.reject.reason.wizard'
    _description = "Reject reason wizard"

    name = fields.Char(string="Additional Information")

    def action_reject_order(self):
        if active_obj := self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id')):
            if self.env.context.get('active_model') == 'purchase.order':
                active_obj.write({'state': 'reject'})
            if line_id := active_obj.approval_info_line_ids.filtered(
                    lambda x: x.level == active_obj.level and x.status == 'to_approve'):
                line_id.write({
                    'status'       : 'rejected',
                    'additional_info': self.name,
                    'approval_date': fields.Datetime.now(),
                    'approval_by'  : self.env.user,
                })

                if line_id.group_ids:
                    users = self.env['res.users'].search([('groups_id', 'in', line_id.group_ids.ids)])
                else:
                    users = line_id.user_ids

                for user in users:
                    if activities := active_obj._get_user_activities(user):
                        activities.unlink()
            if next_line_ids := active_obj.approval_info_line_ids.filtered(lambda x: x.status == 'to_approve'):
                next_line_ids.write({
                    'status': 'canceled',
                    'additional_info': _('Canceled by previous Rejected Approval'),
                    'approval_date': fields.Datetime.now()
                })
