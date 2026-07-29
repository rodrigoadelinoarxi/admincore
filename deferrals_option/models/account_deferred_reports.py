from dateutil.relativedelta import relativedelta

from odoo import fields, models, _


class DeferredReportCustomHandler(models.AbstractModel):
    _inherit = 'account.deferred.report.handler'

    def _is_pt_company(self):
        return self.env.company.account_fiscal_country_id.code == 'PT'

    def _get_domain(self, report, options, filter_already_generated=False, filter_not_started=False):
        domain = report._get_options_domain(options, "from_beginning")
        if self._get_deferred_report_type() == 'expense':
            account_types = ('expense', 'expense_depreciation', 'expense_direct_cost')
            deferred_account_code_domain = ('account_id.code', '=like', '28%')
        else:
            account_types = ('income', 'income_other')
            deferred_account_code_domain = ('account_id.code', '=like', '272%')

        if self._is_pt_company():
            domain += [
                ('move_id.asset_id', '!=', False),
                deferred_account_code_domain,
                ('move_id.date', '<=', options['date']['date_to']),
            ]
            if filter_already_generated:
                domain += [
                    '!',
                        ('move_id.deferred_move_ids', 'any', [
                            ('date', '=', options['date']['date_to']),
                            '|',
                                ('state', '=', 'posted'),
                                '&',
                                    ('auto_post', '=', 'at_date'),
                                    ('date', '>=', fields.Date.context_today(self)),
                        ])
                ]
            return domain

        domain += [
            '|',
                '&',
                    ('move_id.asset_id', '!=', False),
                    deferred_account_code_domain,
                '&',
                    ('move_id.asset_id', '=', False),
                    '|',
                        ('account_id.account_type', 'in', account_types),
                        deferred_account_code_domain,
            ('deferred_start_date', '!=', False),
            ('deferred_end_date', '!=', False),
            ('deferred_end_date', '>=', options['date']['date_from']),
            ('move_id.date', '<=', options['date']['date_to']),
        ]
        domain += ['|', ('move_id.asset_id', '!=', False)] + self._get_domain_fully_inside_period(options)
        if filter_already_generated:
            domain += [
                ('deferred_end_date', '>=', options['date']['date_from']),
                '!',
                    ('move_id.deferred_move_ids', 'any', [
                        ('date', '=', options['date']['date_to']),
                        '|',
                            ('state', '=', 'posted'),
                            '&',
                                ('auto_post', '=', 'at_date'),
                                ('date', '>=', fields.Date.context_today(self)),
                    ])
        ]
        if filter_not_started:
            domain += [('deferred_start_date', '>', options['date']['date_to'])]
        return domain

    def action_audit_cell(self, options, params):
        if not self._is_pt_company():
            return super().action_audit_cell(options, params)

        report = self.env['account.report'].browse(options['report_id'])
        column_values = next(
            (column for column in options['columns'] if (
                column['column_group_key'] == params.get('column_group_key')
                and column['expression_label'] == params.get('expression_label')
            )),
            None
        )
        if not column_values:
            return

        column_date_from = fields.Date.to_date(column_values['date_from'])
        column_date_to = fields.Date.to_date(column_values['date_to'])
        report_date_from = fields.Date.to_date(options['date']['date_from'])
        report_date_to = fields.Date.to_date(options['date']['date_to'])

        if column_values['expression_label'] in ('not_started', 'later'):
            column_date_from = report_date_to + relativedelta(days=1)
        if column_values['expression_label'] == 'before':
            column_date_to = report_date_from - relativedelta(days=1)

        _grouping_model, grouping_record_id = report._get_model_info_from_id(params.get('calling_line_dict_id'))

        original_move_lines_domain = self._get_domain(
            report, options, filter_not_started=column_values['expression_label'] == 'not_started'
        )
        if grouping_record_id:
            original_move_lines_domain.append(('account_id', '=', grouping_record_id))

        original_moves = self.env['account.move.line'].search(original_move_lines_domain).move_id

        domain = [
            ('move_id.asset_id', '!=', False),
            ('move_id', 'in', original_moves.ids),
        ]
        if column_values['expression_label'] == 'not_started':
            domain += [('move_id.date', '>', report_date_to)]
        elif column_values['expression_label'] == 'before':
            domain += [('move_id.date', '<', report_date_from)]
        elif column_values['expression_label'] == 'later':
            domain += [('move_id.date', '>', report_date_to)]
        elif column_values['expression_label'] == 'total':
            domain += [('move_id.date', '<=', report_date_to)]
        else:
            domain += [
                ('move_id.date', '>=', column_date_from),
                ('move_id.date', '<=', column_date_to),
            ]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Deferred Entries'),
            'res_model': 'account.move.line',
            'domain': domain,
            'views': [(False, 'list'), (False, 'pivot'), (False, 'graph'), (False, 'kanban')],
            'context': {
                'search_default_account_id': grouping_record_id,
                'expand': True,
            },
        }
