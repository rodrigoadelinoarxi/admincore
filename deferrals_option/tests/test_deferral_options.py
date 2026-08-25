from odoo.addons.account_asset.tests.common import TestAccountAssetCommon
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestDeferralOptions(TestAccountAssetCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # account_asset_type (models/account.py) is driven purely by the account
        # code prefix ('28' -> expense, '272' -> revenue), which the generic
        # minimal CoA used by AccountTestInvoicingCommon doesn't provide -- so
        # the deferral-specific accounts are created explicitly here.
        cls.expense_deferral_account = cls.env['account.account'].create({
            'code': '2812',
            'name': 'Deferred Expenses (test)',
            'account_type': 'asset_current',
            'company_ids': [(6, 0, [cls.company_data['company'].id])],
        })
        cls.revenue_deferral_account = cls.env['account.account'].create({
            'code': '2721',
            'name': 'Deferred Revenues (test)',
            'account_type': 'liability_current',
            'company_ids': [(6, 0, [cls.company_data['company'].id])],
        })

    def _create_expense_deferral(self, **kwargs):
        values = {
            'value': 1200.0,
            'periodicity': 'monthly',
            'periods': 12,
            'prorata_computation_type': 'none',
            'account_depreciation_id': self.expense_deferral_account.id,
            'account_depreciation_expense_id': self.company_data['default_account_expense'].id,
            'movement_type': 'credit',
            # Deliberately in the future: validate() auto-posts any
            # depreciation move whose date has already passed, which would
            # leave nothing in 'draft' for tests that need to call _post()
            # themselves.
            'acquisition_date': '2030-01-01',
        }
        values.update(kwargs)
        return self.create_asset(**values)

    @staticmethod
    def _post_move(move):
        # The moves generated for a future acquisition_date come back with
        # auto_post scheduling them instead of posting immediately; clear it
        # so the test can post on demand, same pattern as core's own
        # account_asset tests (see test_account_asset.py).
        move.auto_post = 'no'
        move.action_post()

    # -------------------------------------------------------------------
    # account.account: account_asset_type / can_create_asset
    # -------------------------------------------------------------------

    def test_account_asset_type_expense(self):
        self.assertEqual(self.expense_deferral_account.account_asset_type, 'expense')

    def test_account_asset_type_revenue(self):
        self.assertEqual(self.revenue_deferral_account.account_asset_type, 'revenue')

    def test_account_asset_type_false_for_unrelated_account(self):
        self.assertFalse(self.company_data['default_account_expense'].account_asset_type)

    def test_can_create_asset_extended_to_current_and_liability(self):
        """Core only allows asset_fixed/asset_non_current; this module adds
        asset_current/liability_current so deferral accounts can be selected."""
        self.assertTrue(self.expense_deferral_account.can_create_asset)
        self.assertTrue(self.revenue_deferral_account.can_create_asset)

    # -------------------------------------------------------------------
    # account.asset
    # -------------------------------------------------------------------

    def test_deferral_type_follows_depreciation_account(self):
        asset = self._create_expense_deferral()
        self.assertEqual(asset.deferral_type, 'expense')

    def test_deferral_type_false_for_regular_asset(self):
        asset = self.create_asset(value=1000.0, periodicity='yearly', periods=5)
        self.assertFalse(asset.deferral_type)

    def test_movement_type_default_is_credit(self):
        asset = self._create_expense_deferral()
        self.assertEqual(asset.movement_type, 'credit')

    # -------------------------------------------------------------------
    # Depreciation board / posted move lines
    # -------------------------------------------------------------------

    def test_expense_deferral_generates_monthly_moves(self):
        asset = self._create_expense_deferral()
        asset.validate()
        self.assertEqual(asset.state, 'open')
        self.assertEqual(len(asset.depreciation_move_ids), 12)
        self.assertTrue(all(
            move.depreciation_value == 100.0 for move in asset.depreciation_move_ids
        ))

    def test_expense_deferral_move_lines_get_deferred_dates(self):
        """The 'expense'/'revenue' branch of
        AccountMove._prepare_move_for_asset_depreciation stamps
        deferred_start_date/deferred_end_date on both generated lines."""
        asset = self._create_expense_deferral()
        asset.validate()
        first_move = asset.depreciation_move_ids.sorted('date')[0]
        self._post_move(first_move)

        self.assertEqual(first_move.state, 'posted')
        for line in first_move.line_ids:
            self.assertTrue(line.deferred_start_date)
            self.assertTrue(line.deferred_end_date)

    def test_movement_type_debit_uses_reversed_cumulative_logic(self):
        """movement_type == 'debit' swaps which line is debited/credited in
        _prepare_move_for_asset_depreciation, which flips the sign of the
        core-computed depreciation_value (-100 instead of +100 per period).
        _compute_depreciation_cumulative_value's debit branch uses the
        mirror-image formula (remaining += dep_value, depreciated -=
        dep_value) to compensate, so the user-facing remaining/depreciated
        values still move the same way as a normal credit-side asset."""
        asset = self._create_expense_deferral(movement_type='debit')
        asset.validate()
        first_move = asset.depreciation_move_ids.sorted('date')[0]
        self.assertEqual(first_move.depreciation_value, -100.0)
        self._post_move(first_move)

        self.assertEqual(first_move.asset_remaining_value, 1100.0)
        self.assertEqual(first_move.asset_depreciated_value, 100.0)

    # -------------------------------------------------------------------
    # account.move / account.move.line
    # -------------------------------------------------------------------

    def test_move_display_name_relabeled_for_deferral(self):
        asset = self._create_expense_deferral()
        asset.validate()
        move = asset.depreciation_move_ids.sorted('date')[0]

        self.assertEqual(move.asset_id_display_name, 'Deferral')

    def test_regular_asset_move_display_name_unaffected(self):
        asset = self.create_asset(value=1000.0, periodicity='yearly', periods=5)
        asset.validate()
        move = asset.depreciation_move_ids.sorted('date')[0]

        self.assertEqual(move.asset_id_display_name, 'Asset')
        self.assertFalse(move.deferral_exists)

    def test_deferral_exists_flag_from_move_line_asset_ids(self):
        """deferral_exists looks at account.move.line.asset_ids (the M2M a
        vendor bill line gets populated with once it generates an asset) --
        not the depreciation move's own singular asset_id -- so it's
        exercised directly here rather than through a depreciation move."""
        asset = self._create_expense_deferral()
        expense_account = self.company_data['default_account_expense']
        misc_move = self.env['account.move'].create({
            'move_type': 'entry',
            'journal_id': self.company_data['default_journal_misc'].id,
            'line_ids': [
                (0, 0, {
                    'account_id': expense_account.id,
                    'debit': 100.0, 'credit': 0.0,
                    'asset_ids': [(6, 0, asset.ids)],
                }),
                (0, 0, {'account_id': expense_account.id, 'debit': 0.0, 'credit': 100.0}),
            ],
        })
        # deferral_exists isn't itself a computed field -- it's only set as a
        # side effect inside _compute_asset_ids -- so force that compute to
        # run by reading one of its actual computed fields first, the same
        # way opening the move's form view would.
        self.assertTrue(misc_move.count_asset)
        self.assertTrue(misc_move.deferral_exists)

    def test_has_deferred_compatible_account_for_28x_code(self):
        """The 28x/272x deferral accounts aren't 'expense'/'income'
        internal_group accounts, so core's own check would say no; this
        module's override recognizes them by code prefix instead."""
        asset = self._create_expense_deferral()
        asset.validate()
        first_move = asset.depreciation_move_ids.sorted('date')[0]
        self._post_move(first_move)

        deferral_line = first_move.line_ids.filtered(lambda l: l.account_id == self.expense_deferral_account)
        self.assertTrue(deferral_line)
        self.assertTrue(deferral_line._has_deferred_compatible_account())
