from odoo import api, fields, models, _


class PlanningSend(models.TransientModel):
	_inherit = 'planning.send'

	def action_publish(self):
		res = super(PlanningSend, self).action_publish()
		for slot in self.slot_ids:
			slot.action_publish()
		return res
