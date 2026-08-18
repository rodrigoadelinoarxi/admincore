from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class HrContract(models.Model):
    # hr.contract was merged into hr.version in Odoo 19 (ver [[migracao-admincore-17-19]]
    # 12º achado); 'state' (draft/open/close) doesn't exist on hr.version anymore,
    # replaced by the computed 'is_current' boolean - closest equivalent to the old
    # state == 'open' filter (2026-08-18).
    _inherit = 'hr.version'

    @api.model
    def scheduler_manage_contract_expiration(self):
        params = self.env['ir.config_parameter'].sudo()
        delay_alert_contract = int(params.get_param('casperventures.delay_alert_hr_contract', default=30))
        date_today = fields.Date.from_string(fields.Date.today())
        outdated_days = fields.Date.to_string(date_today + relativedelta(days=+delay_alert_contract))
        reminder_activity_type = self.env.ref(
            'casperventures.mail_act_hr_contract_to_renew', raise_if_not_found=False) or self.env['mail.activity.type']
        nearly_expired_contracts = self.search([
            ('date_end', '<', outdated_days),
            ('is_current', '=', True)
        ]).filtered(lambda nec: reminder_activity_type not in nec.activity_ids.activity_type_id)

        for contract in nearly_expired_contracts:
            contract.activity_schedule(
                'casperventures.mail_act_hr_contract_to_renew', contract.date_end, user_id=contract.hr_responsible_id.id
            )

    def run_scheduler_contract(self):
        self.scheduler_manage_contract_expiration()
