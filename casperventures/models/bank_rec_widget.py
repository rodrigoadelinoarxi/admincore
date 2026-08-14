from odoo import _, api, models, Command
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

ANALYTIC_REQUIRED_ACCOUNT_TYPES = [
    'expense', 'income_other', 'income', 'expense_depreciation', 'expense_direct_cost'
]


class BankRecWidget(models.Model):
    _name = "bank.rec.widget"
    _inherit = "bank.rec.widget"

    def _check_analytic_distribution_required(self):
        """Block validation of the bank reconciliation widget if a line hitting a class 6/7-like
        (expense/income) account has no analytic distribution.

        NOTE: as of the current bank_rec_widget implementation, reconciliation is posted through
        `_action_validate()` (called by `_js_action_validate()` / `_action_to_check()`), not
        through `js_action_reconcile_st_line` anymore. This check is called from `_action_validate`
        so it actually runs.
        """
        if self.env.context.get('force_certified_import'):
            return
        st_line = self.st_line_id
        if st_line.journal_id == st_line.company_id.currency_exchange_journal_id:
            return
        offending_lines = self.line_ids.filtered(
            lambda l: l.flag not in ('liquidity', 'exchange_diff', 'tax_line', 'early_payment')
            and not l.analytic_distribution
            and l.account_id.account_type in ANALYTIC_REQUIRED_ACCOUNT_TYPES
        )
        if offending_lines:
            raise ValidationError(_(
                "To post this invoice, you'll need to have an analytic account on every line!"
            ))

    def _action_validate(self):
        self._check_analytic_distribution_required()
        return super()._action_validate()

    @api.model
    def js_action_reconcile_st_line(self, st_line_id, params):
        st_line = self.env['account.bank.statement.line'].browse(st_line_id)

        # Remove the existing lines.
        move = st_line.move_id

        # Update the move.
        move_ctx = move.with_context(
            skip_invoice_sync=True,
            skip_invoice_line_sync=True,
            skip_account_move_synchronization=True,
            force_delete=True,
        )
        move_ctx.write({'line_ids': [Command.clear()] + params['command_list']})

        # REIMPLEMENTATION: BLOCK RECONCILIATION IF ANALYTIC DISTRIBUTION IS FALSE
        account_type_list = [
            'expense', 'income_other', 'income', 'expense_depreciation', 'expense_direct_cost'
        ]
        if not self.env.context.get('force_certified_import'):
            for acc_move in move_ctx.filtered(lambda m: m.journal_id != m.company_id.currency_exchange_journal_id):
                if acc_move.invoice_line_ids.filtered_domain([
                    ('analytic_distribution', '=', False),
                    ('display_type', '=', 'product'),
                    ('account_id.account_type', 'in', account_type_list)
                ]):
                    raise ValidationError(_(
                        "To post this invoice, you'll need to have an analytic account on every line!"
                    ))
        # END REIMPLEMENTATION

        if move_ctx.state == 'draft':
            move_ctx.action_post()

        # Perform the reconciliation.
        for index, counterpart_aml_id in params['to_reconcile']:
            counterpart_aml = self.env['account.move.line'].browse(counterpart_aml_id)

            # REIMPLEMENTATION: BLOCK RECONCILIATION IF ANALYTIC DISTRIBUTION IS FALSE
            account_type_list = [
                'expense', 'income_other', 'income', 'expense_depreciation', 'expense_direct_cost'
            ]
            if counterpart_aml.filtered_domain([
                ('analytic_distribution', '=', False),
                ('display_type', '=', 'product'),
                ('account_id.account_type', 'in', account_type_list)
            ]):
                raise ValidationError(_(
                    "To post this invoice, you'll need to have an analytic account on every line!"
                ))
            # REIMPLEMENTATION END

            (move_ctx.line_ids.filtered(lambda x: x.sequence == index) + counterpart_aml).reconcile()

        # Fill missing partner.
        st_line.with_context(skip_account_move_synchronization=True).partner_id = params['partner_id']

        # Create missing partner bank if necessary.
        if st_line.account_number and st_line.partner_id and not st_line.partner_bank_id:
            st_line.partner_bank_id = st_line._find_or_create_bank_account()

        # Refresh analytic lines.
        move.line_ids.analytic_line_ids.unlink()
        move.line_ids._create_analytic_lines()
