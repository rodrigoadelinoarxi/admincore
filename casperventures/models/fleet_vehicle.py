from dateutil.relativedelta import relativedelta

from odoo import fields, models
from odoo.tools import float_compare


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    service_mileage_interval = fields.Float(default=10000)
    insurance = fields.Date(
        compute='_get_insurance', string='Last Insurance Date',
        help='Last insurance date of the vehicle at the moment of this log'
    )
    km_warning = fields.Integer()

    def _get_odometer(self):
        res = super(FleetVehicle, self)._get_odometer()
        params = self.env['ir.config_parameter'].sudo()
        service_mileage_alert = int(params.get_param('casperventures.fleet_km_between_service', default=500))
        for rec in self.filtered(lambda v: v.vehicle_type == 'car'):
            # Check Odometer or Last Service Date
            date_alert = int(params.get_param('hr_fleet.delay_alert_contract', default=30))
            vehicle_service = rec.env['fleet.vehicle.log.services'].search([
                ('vehicle_id', '=', rec.id),
                ('state', 'in', ('running', 'done')),
                ('service_type_id', '=', self.env.ref('casperventures.fleet_service_type_service').id),
            ], limit=1, order='date desc')
            needs_service_based_on_odometer = float_compare(
                rec.odometer, rec.service_mileage_interval - service_mileage_alert + vehicle_service.odometer, 2
            ) >= 0
            last_service_date = (vehicle_service.date or rec.acquisition_date)
            needs_service_based_on_date = last_service_date + relativedelta(
                years=1, days=-date_alert) <= fields.Date.today()

            if needs_service_based_on_odometer or needs_service_based_on_date:
                inspection_act_type = self.env.ref('casperventures.mail_act_fleet_to_register_service')
                if not rec.activity_ids.filtered(lambda a: a.activity_type_id == inspection_act_type):
                    rec.activity_schedule(
                        'casperventures.mail_act_fleet_to_register_service',
                        fields.Date.today() + relativedelta(days=5),
                        user_id=rec.manager_id.id
                    )
        return res

    def _get_insurance(self):
        for record in self:
            vehicle_insurance = self.env['fleet.vehicle.log.contract'].search([
                ('vehicle_id', '=', record.id),
                ('cost_subtype_id', '=', self.env.ref('casperventures.fleet_service_type_insurance').id),
                ('state', '=', 'open')
            ], limit=1, order='expiration_date desc')
            record.insurance = vehicle_insurance.expiration_date if vehicle_insurance else False

    def run_scheduler_fleet(self):
        for rec in self.search([]):
            rec.activity_schedule(
                'casperventures.mail_act_fleet_to_register_data',
                fields.Date.today() + relativedelta(days=5),
                user_id=rec.manager_id.id
            )
