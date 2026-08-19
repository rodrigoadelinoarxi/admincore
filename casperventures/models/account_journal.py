from odoo import models, fields, api, _
from odoo.tools import date_utils
from odoo.exceptions import ValidationError
import datetime
import logging

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    default_ecommerce_analytic_account = fields.Many2one('account.analytic.account')
    default_analytic_account = fields.Many2one('account.analytic.account')

    nos_alive_default = fields.Boolean(string="NOS Alive default journal")

    color_journal = fields.Char(string="Color", default="#000000")
    default_donation_description = fields.Char(string="Default description", default="Donation")

    def get_journal_dashboard_datas(self):
        res = self._get_journal_dashboard_data_batched()[self.id]
        return res

    def get_today_move_data(self):
        today = datetime.datetime.today()
        yesterday = date_utils.subtract(today, days=1)

        # {{ object.partner_id.lang }}

        has_statement = self.get_journal_dashboard_datas().get('has_at_least_one_statement')
        model_name = 'account.bank.statement.line' if has_statement else 'account.move'
        move_data_ids = self.env[model_name].search([
            ('date', 'in', [yesterday, today]), ('journal_id', '=', self.id), ('state', 'in', ['posted', 'confirm'])
        ])
        if model_name == 'account.move':
            return [{
                'date': data_id.date,
                'description': data_id.ref,
                'partner_name': data_id.partner_id.name,
                'amount': data_id.amount_total_signed,
                'currency_id': data_id.currency_id,
            } for data_id in move_data_ids]
        return [{
            'date': data_id.date,
            'description': data_id.payment_ref,
            'partner_name': data_id.partner_id.name,
            'amount': data_id.amount,
            'currency_id': data_id.currency_id,
        } for data_id in move_data_ids]


    @api.onchange('nos_alive_default')
    def check_unique_nos_journal(self):
        for journal_id in self.ids:
            journals = self.env['account.journal'].search([('id', '!=', journal_id), ('nos_alive_default', '=', True)])
            if journals:
                raise ValidationError(_('Only one journal can be the default NOS Alive journal.'))

