from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    email_partner_ids = fields.Many2many('res.partner')
    use_custom_report = fields.Boolean(string="Use Custom Report", default=False,
                                      help="Enable this option to use custom reports for this company")


    def get_bank_journal_data(self):
        journal_list = []
        journal_ids = self.env['account.journal'].sudo().search([('type', '=', 'bank'), ('company_id', '=', self.id)])

        for account_id in journal_ids.mapped('default_account_id'):
            journal_list.append(journal_ids.filtered(lambda l: l.default_account_id == account_id))

        return journal_list

    def get_move_data(self):
        move_list = []

        move_ids = self.env['account.move'].sudo().search([
            ('company_id', '=', self.id),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', '=', 'posted'),
            ('invoice_date', '=', fields.datetime.today())
        ])

        for team_id in move_ids.mapped('team_id'):
            filtered_move_ids = move_ids.filtered(lambda l: l.team_id == team_id)
            move_list.append({
                'team_name'            : team_id.name,
                'len_move_ids'         : len(filtered_move_ids),
                'amount_untaxed_signed': sum(filtered_move_ids.mapped('amount_untaxed_signed')),
                'amount_total_signed'  : sum(filtered_move_ids.mapped('amount_total_signed')),
            })

        return move_list

    def run_daily_position_email(self):
        template_id = self.env.ref('casperventures.mail_template_daily_company_position')

        journals = self.env['account.journal'].search([('account_online_account_id', '!=', False)])
        _logger.info(f"Starting online transaction fetch for {len(journals)} journals.")
        journals.with_context(cron=True)._fetch_online_transactions()
        _logger.info(f"Completed online transaction fetch for journals.")

        for company_id in self.env['res.company'].search([]):
            if responsible_emails := filter(None, company_id.email_partner_ids.mapped('email')):
                template_id.with_company(company_id).send_mail(
                    company_id.id,
                    force_send=True,
                    email_layout_xmlid='mail.mail_notification_light',
                    email_values={
                        'email_to': ','.join(responsible_emails),
                    }
                )

    def get_sum_availabilities_total_to_eur(self):
        availabilities = self.get_sum_availabilities_of_current_balances()
        current_usd_exchange_rate = self.env['res.currency'].search([('name', '=', 'USD')]).rate
        total_in_eur = 0

        if 1 in availabilities:
            total_in_eur += availabilities[1]['sum']

        if 2 in availabilities:
            total_in_eur += availabilities[2]['sum'] * current_usd_exchange_rate

        return total_in_eur

    # Replaced by get_sum_availabilities_of_current_balances
    def get_sum_availabilities(self):
        sum_totals_by_currency = {}
        for journal_ids in self.get_bank_journal_data():
            multiple_journals = True if len(journal_ids) > 1 else False

            for journal_id in journal_ids:
                journal_data = journal_id.get_journal_dashboard_datas()
                has_statement = journal_data.get('has_at_least_one_statement')
                currency_id = journal_id.currency_id.id
                currency_symbol = journal_id.currency_id.symbol
                if currency_id:
                    if currency_id not in sum_totals_by_currency:
                        sum_totals_by_currency[currency_id] = {'sum': 0.00, 'symbol': currency_symbol}

                    if has_statement:
                        sum_totals_by_currency[currency_id]['sum'] += self.convert_balance_to_float(
                            journal_data.get('last_balance', 0))
                    elif not multiple_journals:
                        sum_totals_by_currency[currency_id]['sum'] += self.convert_balance_to_float(
                            journal_data.get('account_balance', 0))

            if multiple_journals and journal_ids[0].currency_id.id:
                sum_totals_by_currency[journal_ids[0].currency_id.id]['sum'] += self.convert_balance_to_float(
                    journal_ids[0].get_journal_dashboard_datas().get('account_balance', 0))
        return sum_totals_by_currency

    def get_sum_availabilities_of_current_balances(self):
        new_total_by_currency = {}
        for journal_ids in self.get_bank_journal_data():

            for journal_id in journal_ids:
                journal_data = journal_id.get_journal_dashboard_datas()
                currency_id = journal_id.currency_id.id
                currency_symbol = journal_id.currency_id.symbol
                if currency_id:
                    if currency_id not in new_total_by_currency:
                        new_total_by_currency[currency_id] = {'sum': 0.00, 'symbol': currency_symbol}

                    new_total_by_currency[currency_id]['sum'] += self.convert_balance_to_float(
                        journal_data.get('account_balance', 0))

        return new_total_by_currency

    def convert_balance_to_float(self, val):
        balance_str = val

        # Check if the balance is negative
        is_negative = balance_str.startswith('-')

        # Convert the balance string to a numeric format
        cleaned_balance_str = balance_str.replace('€', '').replace('$', '').replace('£', '').replace('-', '').replace('\ufeff', '').replace('\xa0', '').strip()

        try:
            before_last_two_digits = cleaned_balance_str[-3]
            if before_last_two_digits == ',':
                cleaned_balance_str = cleaned_balance_str.replace('.', '').replace(',', '.').strip()
            elif before_last_two_digits == '.':
                cleaned_balance_str = cleaned_balance_str.replace(',', '').strip()
        except Exception as e:
            _logger.warning(f"Error processing balance string '{balance_str}': {e}")

        balance_float = float(cleaned_balance_str)

        # If it was negative, multiply by -1
        if is_negative:
            balance_float *= -1

        return balance_float
