from odoo import fields, models, api, _


class ResCompany(models.Model):
	_inherit = 'res.company'

	automatic_timesheets = fields.Boolean(string='Automatic Timesheets', help='If checked, timesheets will be created automatically when a planning slot is published or sent.')
