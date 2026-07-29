from odoo import api, fields, models, _, Command


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approval_level_id = fields.Many2one(
        'sh.purchase.approval.config', string="Approval Level", compute="compute_approval_level")
    state = fields.Selection(
        selection_add=[('waiting_for_approval', 'Waiting for Approval'), ('purchase',), ('reject', 'Rejected'), ('purchase',)])
    level = fields.Integer(string="Next Approval Level", readonly=True)
    user_ids = fields.Many2many('res.users', string="Users", readonly=True)
    group_ids = fields.Many2many('res.groups', string="Groups", readonly=True)
    user_is_approver = fields.Boolean(compute="compute_user_is_approver", search='_search_user_is_approver')
    approval_info_line_ids = fields.One2many(
        'sh.approval.info', 'purchase_order_id', readonly=True)

    def compute_user_is_approver(self):
        for rec in self:
            rec.user_is_approver = self.env.user in rec.user_ids or any(
                group in self.env.user.groups_id for group in rec.group_ids
            )

    def _search_user_is_approver(self, operator, value):
        results = []
        if value:
            results = self.env['purchase.order'].search([
                '|', ('user_ids', 'in', [self.env.user.id]), ('group_ids', 'in', self.env.user.groups_id.ids)]
            ).ids
        return [('id', operator, results)]

    def button_confirm(self):
        if lines := self.approval_level_id.purchase_approval_line_ids.sorted('level'):
            for line in lines:
                approval_values = []
                if line.approve_by == 'group':
                    approval_values.append((0, 0, {
                        'level'    : line.level,
                        'user_ids' : False,
                        'group_ids': [(6, 0, line.group_ids.ids)],
                    }))
                elif line.approve_by == 'user':
                    approval_values.append((0, 0, {
                        'level'    : line.level,
                        'user_ids' : [(6, 0, line.user_ids.ids)],
                        'group_ids': False,
                    }))
                self.write({
                    'state'    : 'waiting_for_approval',
                    'level'    : lines[0].level,
                    'group_ids': [(6, 0, lines[0].group_ids.ids)] if lines[0].approve_by == 'group' else False,
                    'user_ids' : [(6, 0, lines[0].user_ids.ids)] if lines[0].approve_by == 'user' else False,
                    'approval_info_line_ids': approval_values
                })
            if lines[0].approve_by == 'group':
                users = lines[0].group_ids.mapped('users')
            else:
                users = lines[0].user_ids
            self.create_activities(users)
        else:
            super(PurchaseOrder, self).button_confirm()

    def _get_user_activities(self, user):
        domain = [
            ('res_model', '=', 'purchase.order'),
            ('res_id', 'in', self.ids),
            ('activity_type_id', '=', self.env.ref('sh_purchase_dynamic_approval.mail_activity_data_approval').id),
            ('user_id', '=', user.id)
        ]
        activities = self.env['mail.activity'].search(domain)
        return activities

    @api.depends('amount_untaxed', 'amount_total')
    def compute_approval_level(self):
        for rec in self:
            if rec.company_id.approval_based_on:
                min_amount = rec.company_id.approval_based_on == 'untaxed_amount' and rec.amount_untaxed or \
                             rec.company_id.approval_based_on == 'total' and rec.amount_total or 0
                purchase_approvals = rec.env['sh.purchase.approval.config'].search([
                    ('min_amount', '<=', min_amount),
                    ('company_ids', 'in', [rec.env.company.id])
                ], order='sequence', limit=1)
                rec.approval_level_id = purchase_approvals

    def action_approve_order(self, confirm_order=True):
        if info := self.approval_info_line_ids.filtered(lambda x: x.level == self.level and x.status == 'to_approve'):
            info.write({
                'status'       : 'approved',
                'approval_date': fields.Datetime.now(),
                'approval_by'  : self.env.user,
            })

        line_id = self.env['sh.purchase.approval.line'].search(
            [('purchase_approval_config_id', '=', self.approval_level_id.id),
             ('level', '=', self.level)])
        next_line = self.env['sh.purchase.approval.line'].search([
            ('purchase_approval_config_id', '=', self.approval_level_id.id),
            ('level', '>', self.level)
        ], limit=1, order='level')

        if line_id.approve_by == 'group':
            users = self.env['res.users'].search([('groups_id', 'in', line_id.group_ids.ids)])
        else:
            users = line_id.user_ids
        if activity := self._get_user_activities(self.env.user):
            activity.action_done()
        for user in users:
            if activities := self._get_user_activities(user):
                activities.unlink()

        if next_line:
            if next_line.approve_by == 'group':
                next_users = self.env['res.users'].search([('groups_id', 'in', next_line.group_ids.ids)])
                self.write({
                    'level'    : next_line.level,
                    'user_ids' : False,
                    'group_ids': [Command.set(next_line.group_ids.ids)],
                })
            elif next_line.approve_by == 'user':
                next_users = next_line.user_ids
                self.write({
                    'level'    : next_line.level,
                    'user_ids' : [Command.set(next_line.user_ids.ids)],
                    'group_ids': False
                })
            self.create_activities(next_users)
        else:
            self.write({
                'level'    : False,
                'group_ids': False,
                'user_ids' : False,
                'state'    : 'sent',
            })
            if confirm_order:
                super(PurchaseOrder, self).button_confirm()

    def get_approval_notification_info(self, user):
        return (user.partner_id, 'sh_notification_info', {
            'title'  : _('Notification'),
            'message': _('You have an approval notification for the Purchase Order %s', self.name)
        })

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    def create_activities(self, users):
        for user in users:
            self.activity_schedule(
                'sh_purchase_dynamic_approval.mail_activity_data_approval',
                user_id=user.id)
