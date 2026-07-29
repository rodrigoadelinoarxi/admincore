import logging

from odoo import models, _, fields
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def check_and_create_default_analytic_distribution(self, lines, analytic_account):
        lines.write({
            'analytic_line_ids'    : [(0, 0, {
                'name'      : analytic_account.name,
                'account_id': analytic_account.id,
                'amount'    : 100,
                'company_id': analytic_account.company_id and analytic_account.company_id.id
            })],
            'analytic_distribution': {
                analytic_account.id: 100
            }
        })

    def _post(self, soft=True):
        account_type_list = [
            'expense', 'income_other', 'income', 'expense_depreciation', 'expense_direct_cost'
        ]
        if not self.env.context.get('force_certified_import'):
            for move in self:
                if (move.invoice_line_ids.mapped(
                        'sale_line_ids.order_id.website_id') or self.env.context.get(
                    'payment_transaction')) and move.journal_id.default_ecommerce_analytic_account:
                    lines = move.invoice_line_ids.filtered_domain([
                        ('analytic_distribution', '=', False),
                        ('display_type', '=', 'product'),
                        ('account_id.account_type', 'in', account_type_list)
                    ])
                    self.check_and_create_default_analytic_distribution(lines,
                                                                        move.journal_id.default_ecommerce_analytic_account)
                elif move.journal_id.default_analytic_account:
                    lines = move.invoice_line_ids.filtered_domain([
                        ('analytic_distribution', '=', False),
                        ('display_type', '=', 'product'),
                        ('account_id.account_type', 'in', account_type_list)
                    ])
                    self.check_and_create_default_analytic_distribution(lines,
                                                                        move.journal_id.default_analytic_account)
                if not self.env.context.get(
                        'payment_transaction') and move.journal_id != move.company_id.currency_exchange_journal_id:
                    if move.invoice_line_ids.filtered_domain([
                        ('analytic_distribution', '=', False),
                        ('display_type', '=', 'product'),
                        ('account_id.account_type', 'in', account_type_list)
                    ]):
                        raise ValidationError(_(
                            "To post this invoice, you'll need to have an analytic account on every line!"
                        ))
        return super(AccountMove, self)._post(soft)
