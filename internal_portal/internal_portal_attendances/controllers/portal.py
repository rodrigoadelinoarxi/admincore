from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):
	def _prepare_portal_layout_values(self):
		values = super(CustomerPortal, self)._prepare_portal_layout_values()
		if request.env.user.has_group('internal_portal_attendances.group_internal_portal_attendances'):
			employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)])
			values['employee_id'] = employee_id
			values['attendance_state'] = employee_id.attendance_state
		else:
			values['attendance_state'] = False
		return values

	@http.route(['/my/internal/attendance'], type='http', auth="user", website=True)
	def portal_my_attendance(self, **kw):
		values = self._prepare_portal_layout_values()
		return request.render("internal_portal_attendances.internal_portal_attendances_check_in_out", values)

	@http.route(['/my/internal/attendance/check-in-out'], type='http', auth="user", website=True)
	def portal_my_attendance_check_in_out(self, **kw):
		values = self._prepare_portal_layout_values()
		employee_id = request.env['hr.employee'].sudo().browse(values['employee_id'].id)

		try:
			employee_id._attendance_action_change()
			values['attendance_state'] = employee_id.attendance_state
		except Exception as e:
			request.env.cr.rollback()
			values.update({'errors': e})
			return request.render("internal_portal_attendances.internal_portal_attendances_check_in_out", values)
		return request.redirect('/my')
