# from odoo.addons.casperventures.scripts.update_amount_account_analytic_by_employee import update_analytic_lines
# update_analytic_lines(self)

from odoo import _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


def update_analytic_lines(self):
    lines = self.env['account.analytic.line'].search([('employee_id', '!=', False)])
    missing_lines = []
    _logger.info(f'Line found: {missing_lines}')
    for line in lines:
        if line.unit_amount <= 0 or line.employee_id.hourly_cost <= 0:
            _logger.info(f'{line.employee_id.name} - analytic item id.{line.id} - {line.name} not updated')
            missing_lines += [
                {'id': line.id, 'employee_id': line.employee_id, 'employee_id.name': line.employee_id.name,
                 'employee_id.hourly_cost': line.employee_id.hourly_cost, 'amount': line.amount}]
            continue
        line.amount = line.unit_amount * line.employee_id.hourly_cost * -1
        _logger.info(f'{line.employee_id.name} - Updating amount for analytic item id.{line.id} - {line.name}: €{line.amount}')
        self.env.cr.commit()
    if len(missing_lines):
        _logger.info(f'Missing {len(missing_lines)} lines  from {len(lines)}: \n {missing_lines}')
