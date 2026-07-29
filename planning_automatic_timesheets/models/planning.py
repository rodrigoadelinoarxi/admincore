from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.addons.resource.models.utils import Intervals
from odoo.osv import expression

import pytz

PLANNING_SLOT_FIELDS_TO_VALIDATE = {
	'resource_id': _("You need to select a resource in order to proceed."),
	'project_id': _("You need to select a project in order to proceed."),
	'allocated_hours': _("You need to allocate hours in order to proceed.")
}


def validate_planning_slot_fields(data):
	"""
		Validate the fields of a planning slot and raise an error if any of them is missing.

		We don't want to make the fields required in the model because we want to be able to create
		planning slots without any of the fields filled in, in case the boolean automatic_timesheets
		is set to False.
	"""
	for field, message in PLANNING_SLOT_FIELDS_TO_VALIDATE.items():
		if not getattr(data, field):
			raise UserError(message)
	return True


class Planning(models.Model):
	_inherit = 'planning.planning'
	slot_ids = fields.Many2many('planning.slot')

	def _send_planning(self,slots=False, message=None, employees=False):
		res = super(Planning, self)._send_planning(slots, message, employees)
		for planning in self:
			for slot in planning.slot_ids:
				slot.create_timesheet()
		return res


class PlanningSlot(models.Model):
	_inherit = 'planning.slot'

	company_has_automatic_timesheets = fields.Boolean(related='company_id.automatic_timesheets', readonly=True)
	task_id = fields.Many2one('project.task')

	def create_timesheet(self):
		"""
			Create a timesheet for the current planning slot to register the hours for the user.
		"""
		self.remove_linked_timesheets()
		start_datetime = self.start_datetime.date()
		start_datetime_day = start_datetime.day

		end_datetime = self.end_datetime.date()
		end_datetime_day = end_datetime.day

		on_same_day = start_datetime_day == end_datetime_day

		employee = self.env['hr.employee'].search([('resource_id', '=', self.resource_id.id)], limit=1)

		if on_same_day:
			a = self.env['account.analytic.line'].create({
				'is_timesheet'		: True,
				'name'				: self.project_id.name,
				'display_name'		: self.project_id.display_name,
				'employee_id'		: employee.id,
				'project_id'		: self.project_id.id,
				'company_id'		: self.project_id.company_id and self.project_id.company_id.id or self.env.company.id,
				'task_id'			: self.task_id.id if self.task_id else False,
				'planning_slot_id'	: self.id,
				'date'				: start_datetime,
				'unit_amount'		: self.allocated_hours
			})
			print(a)
		else:
			days_difference = (end_datetime - start_datetime).days + 1
			to_allocate_time = self.allocated_hours
			current_date = self.start_datetime

			for day in range(days_difference):
				if not to_allocate_time:
					break
				start_utc = pytz.utc.localize(current_date.replace(hour=00, minute=00, second=00))
				end_utc = pytz.utc.localize(current_date.replace(hour=23, minute=59, second=59))

				work_intervals = employee.resource_calendar_id._work_intervals_batch(start_utc, end_utc, employee.resource_id)
				interval = Intervals([(start_utc, end_utc, self.env['resource.calendar.attendance'])])

				work_intervals = interval & work_intervals[employee.resource_id.id]

				current_day_time = sum(
					(stop - start).total_seconds() / 3600
					for start, stop, _resource in work_intervals
				)

				allocate_time = min(to_allocate_time, current_day_time)
				to_allocate_time -= allocate_time

				a = self.env['account.analytic.line'].create({
					'is_timesheet'		: True,
					'name'				: self.project_id.name,
					'display_name'		: self.project_id.display_name,
					'employee_id'		: employee.id,
					'project_id'		: self.project_id.id,
					'company_id'		: self.project_id.company_id and self.project_id.company_id.id or self.env.company.id,
					'task_id'			: self.task_id.id if self.task_id else False,
					'planning_slot_id'	: self.id,
					'date'				: current_date.date(),
					'unit_amount'		: allocate_time
				})
				print(a)
				current_date = current_date + timedelta(days=1)

	def action_publish(self):
		res = super(PlanningSlot, self).action_publish()
		for rec in self:
			if rec.company_id.automatic_timesheets and validate_planning_slot_fields(rec):
				rec.create_timesheet()
		return res

	def action_send(self):
		res = super(PlanningSlot, self).action_send()
		for rec in self:
			if rec.company_id.automatic_timesheets and validate_planning_slot_fields(rec):
				rec.create_timesheet()
		return res

	def write(self, vals):
		"""
			In case the user changes the start time / end time of the planning slot / allocated hours,
			we need to update the timesheets accordingly.

			Since we would need to divide the allocated hours between the different days and more..., instead of
			updating the timesheets, we delete them and create new ones.
		"""
		res = super(PlanningSlot, self).write(vals)
		if any([key in vals for key in ['start_datetime', 'end_datetime', 'allocated_hours']]):
			for rec in self.filtered(lambda p: p.state == 'published'):
				if rec.company_id.automatic_timesheets and validate_planning_slot_fields(rec):
					rec.create_timesheet()
		return res

	def unlink(self):
		if self.company_id.automatic_timesheets:
			self.remove_linked_timesheets()
		return super(PlanningSlot, self).unlink()

	def remove_linked_timesheets(self):
		if account_analytic_lines := self.env['account.analytic.line'].search([('planning_slot_id', '=', self.ids)]):
			account_analytic_lines.unlink()

	def _get_timesheet_domain(self):
		"""
			Returns the domain used to fetch the timesheets, None is returned in case there would be no match
		"""
		if not self.project_id:
			return None
		domain = [
			('employee_id', '=', self.employee_id.id),
			('date', '>=', self.start_datetime.date()),
			('date', '<=', self.end_datetime.date())
		]
		domain = expression.AND([[('account_id', '=', self.project_id.analytic_account_id.id)], domain])
		return domain

	def action_unpublish(self):
		res = super(PlanningSlot, self).action_unpublish()
		if self.company_id.automatic_timesheets:
			self.remove_linked_timesheets()
		return res
