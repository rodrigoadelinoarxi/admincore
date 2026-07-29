from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    delay_alert_hr_contract = fields.Integer(
        string='Delay Alert HR Contract Outdated', default=30, config_parameter='casperventures.delay_alert_hr_contract'
    )

    fleet_km_between_services = fields.Integer(
        string='Delay alert service outdated', default=500, config_parameter='casperventures.fleet_km_between_service'
    )
