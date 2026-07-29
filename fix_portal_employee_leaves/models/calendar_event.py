import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Since odoo does the calendar event create with user, we get a permission error when creating a calendar event for a portal user's leave.
        check the _validate_leave_request method in hr_holidays/models/hr_leave.py
        """
        if not self.env.user.has_group('base.group_user'):
            return super(CalendarEvent, self.sudo()).create(vals_list)
        return super(CalendarEvent, self).create(vals_list)
