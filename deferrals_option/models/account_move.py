from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare
from odoo.exceptions import UserError
from odoo import api, models, fields, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    deferral_exists = fields.Boolean(default=False)

    @api.depends('line_ids.asset_ids')
    def _compute_asset_ids(self):
        '''
        Changes the label to Deferral whe the asset is an expense
        :return:
        '''
        super()._compute_asset_ids()
        for record in self:
            if record.asset_id and record.asset_id.deferral_type == 'expense':
                record.asset_id_display_name = _('Deferral')

            if any(asset.deferral_type == 'expense' for asset in record.asset_ids):
                record.deferral_exists = True

    @api.model
    def _prepare_move_for_asset_depreciation(self, vals):
        if vals['asset_id'].movement_type == 'debit':
            missing_fields = {'asset_id', 'amount', 'depreciation_beginning_date', 'date', 'asset_number_days'} - set(vals)
            if missing_fields:
                raise UserError(_('Some fields are missing %s', ', '.join(missing_fields)))
            asset = vals['asset_id']
            analytic_distribution = asset.analytic_distribution
            depreciation_date = vals.get('date', fields.Date.context_today(self))
            company_currency = asset.company_id.currency_id
            current_currency = asset.currency_id
            prec = company_currency.decimal_places
            amount_currency = vals['amount']
            amount = current_currency._convert(amount_currency, company_currency, asset.company_id, depreciation_date)
            # Keep the partner on the original invoice if there is only one
            partner = asset.original_move_line_ids.mapped('partner_id')
            partner = partner[:1] if len(partner) <= 1 else self.env['res.partner']
            depreciation_start_date = vals['depreciation_beginning_date']
            depreciation_end_date = fields.Date.from_string(depreciation_start_date) + relativedelta(days=vals['asset_number_days'] - 1)
            move_line_1 = {
                'name': asset.name,
                'partner_id': partner.id,
                'account_id': asset.account_depreciation_id.id,
                'debit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'credit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'currency_id': current_currency.id,
                'amount_currency': amount_currency,
                'deferred_start_date': depreciation_start_date,
                'deferred_end_date': depreciation_end_date,
            }
            move_line_2 = {
                'name': asset.name,
                'partner_id': partner.id,
                'account_id': asset.account_depreciation_expense_id.id,
                'credit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'debit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'currency_id': current_currency.id,
                'amount_currency': -amount_currency,
                'deferred_start_date': depreciation_start_date,
                'deferred_end_date': depreciation_end_date,
            }
            # Only set the 'analytic_distribution' key if there is an analytic distribution on the asset.
            # Otherwise, it prevents the computation of the analytic distribution.
            if analytic_distribution:
                move_line_1['analytic_distribution'] = analytic_distribution
                move_line_2['analytic_distribution'] = analytic_distribution
            move_vals = {
                'partner_id': partner.id,
                'date': depreciation_date,
                'journal_id': asset.journal_id.id,
                'line_ids': [(0, 0, move_line_1), (0, 0, move_line_2)],
                'asset_id': asset.id,
                'ref': _("%s: Depreciation", asset.name),
                'asset_depreciation_beginning_date': vals['depreciation_beginning_date'],
                'asset_number_days': vals['asset_number_days'],
                'name': '/',
                'asset_value_change': vals.get('asset_value_change', False),
                'move_type': 'entry',
                'currency_id': current_currency.id,
                'company_id': asset.company_id.id,
            }
            return move_vals
        else:
            move_vals = super(AccountMove, self)._prepare_move_for_asset_depreciation(vals)
            asset = vals['asset_id']
            if asset.deferral_type in ('expense', 'revenue'):
                depreciation_start_date = vals['depreciation_beginning_date']
                depreciation_end_date = fields.Date.from_string(depreciation_start_date) + relativedelta(days=vals['asset_number_days'] - 1)
                for command in move_vals.get('line_ids', []):
                    if command[0] == 0 and command[2]:
                        command[2].update({
                            'deferred_start_date': depreciation_start_date,
                            'deferred_end_date': depreciation_end_date,
                        })
            return move_vals


    @api.depends('asset_id', 'depreciation_value', 'asset_id.total_depreciable_value',
                 'asset_id.already_depreciated_amount_import', 'state')
    def _compute_depreciation_cumulative_value(self):
        self.asset_depreciated_value = 0
        self.asset_remaining_value = 0
        # make sure to protect all the records being assigned, because the
        # assignments invoke method write() on non-protected records, which may
        # cause an infinite recursion in case method write() needs to read one
        # of these fields (like in case of a base automation)
        fields = [self._fields['asset_remaining_value'], self._fields['asset_depreciated_value']]
        with self.env.protecting(fields, self.asset_id.depreciation_move_ids):
            for asset in self.asset_id:
                if asset.movement_type == 'debit':
                    depreciated = 0
                    remaining = asset.total_depreciable_value - asset.already_depreciated_amount_import
                    for move in asset.depreciation_move_ids.sorted(lambda mv: (mv.date, mv._origin.id)):
                        if move.state != 'cancel':
                            remaining += move.depreciation_value
                            depreciated -= move.depreciation_value
                        move.asset_remaining_value = remaining
                        move.asset_depreciated_value = depreciated
                else:
                    super(AccountMove, self)._compute_depreciation_cumulative_value()

    @api.model
    def _get_deferred_amounts_by_line(self, lines, periods):
        values = []
        current_periods = [period for period in periods if period[2] == 'current']
        report_period_from = min((period[0] for period in current_periods), default=None)
        report_period_to = max((period[1] for period in current_periods), default=None)
        for line in lines:
            move = self.browse(line['move_id'])
            if move.company_id.account_fiscal_country_id.code == 'PT' and move.asset_id:
                move_date = fields.Date.to_date(move.date)
                balance = line['balance']
                columns = {}
                for period in periods:
                    label = period[2]
                    if label == 'total':
                        columns[period] = balance
                    elif label in ('not_started', 'later'):
                        columns[period] = balance if report_period_to and move_date > report_period_to else 0.0
                    elif label == 'before':
                        columns[period] = balance if report_period_from and move_date < report_period_from else 0.0
                    else:
                        columns[period] = balance if period[0] <= move_date <= period[1] else 0.0

                values.append({
                    **self.env['account.move.line']._get_deferred_amounts_by_line_values(line),
                    **columns,
                })
                continue

            values.extend(super()._get_deferred_amounts_by_line([line], periods))
        return values


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _is_compatible_account(self):
        res = super()._is_compatible_account()
        if not res:
            return self.account_id.code and (self.account_id.code.startswith('272') or self.account_id.code.startswith('28'))
        return res
