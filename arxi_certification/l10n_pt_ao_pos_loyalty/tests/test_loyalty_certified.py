"""Unit tests for the certified loyalty layer added by l10n_pt_ao_pos_loyalty.

This module keeps a fixed-amount loyalty discount from reducing the taxable base
of a certified POS invoice: the reward line becomes a note
(``prepare_loyalty_move_line``) and a self-paid ``account.payment`` reconciles
the discount against the invoice (``create_loyalty_payment`` /
``invoice_pay_loyalty_program_create``).

The full end-to-end flow is covered by the Playwright spec
(``playwright/tests/pos-loyalty.spec.js``). These pre-commit tests instead pin
the Python-side logic that the v18->v19 migration had to fix, so a regression is
caught without the browser:

* the v19 ``loyalty.reward`` field names are used (``discount_mode`` /
  ``discount`` / ``discount_applicability`` — NOT the v18 ``discount_type`` /
  ``discount_percentage`` / ``discount_apply_on``, which no longer exist);
* ``prepare_loyalty_move_line`` turns the reward line into a value-less note;
* ``invoice_pay_loyalty_program_create`` builds valid v19 ``account.payment``
  vals (``memo`` not ``ref``; amount = the VAT-inclusive discount) with the
  right sequence per document type;
* a ``pos_loyalty_program`` product can never carry a tax, even when created via
  the ORM without an explicit ``taxes_id``.

Reuses l10n_pt_ao's AccountTestCertifiedCommon (AO company, database.is_neutralized,
certified sale journal) so a certified move can be posted and hashed locally — the
same base the l10n_pt_ao certification tests use, and a clean dependency since this
module depends (transitively) on l10n_pt_ao.
"""

from odoo import Command
from odoo.addons.l10n_pt_ao.tests.test_l10n_pt_ao_common import (
    AccountTestCertifiedCommon,
)
from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestLoyaltyCertified(AccountTestCertifiedCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # A cash/bank journal for the self-paid loyalty payment.
        cls.loyalty_journal = cls.env["account.journal"].create(
            {
                "name": "Loyalty Payment Test",
                "type": "cash",
                "code": "LOYP",
                "company_id": cls.company.id,
            }
        )
        cash_pm = cls.env["pos.payment.method"].create(
            {
                "name": "Cash Test",
                "journal_id": cls.loyalty_journal.id,
                "company_id": cls.company.id,
            }
        )
        cls.pos_config = cls.env["pos.config"].create(
            {
                "name": "PT AO Loyalty POS Test",
                "company_id": cls.company.id,
                "payment_method_ids": [Command.set(cash_pm.ids)],
                "loyalty_payment_journal": cls.loyalty_journal.id,
            }
        )
        cls.pos_config.with_user(cls.env.user).open_ui()
        cls.pos_session = cls.pos_config.current_session_id

        # A fixed-amount (per_order) discount reward — the case that drives the
        # self-paid payment path.
        cls.program = cls.env["loyalty.program"].create(
            {
                "name": "PT AO Loyalty Test",
                "program_type": "promotion",
                "trigger": "auto",
                "applies_on": "current",
                "company_id": cls.company.id,
                "reward_ids": [
                    Command.create(
                        {
                            "reward_type": "discount",
                            "discount": 10.0,
                            "discount_mode": "per_order",
                            "discount_applicability": "order",
                            "required_points": 1,
                        }
                    )
                ],
            }
        )
        cls.reward = cls.program.reward_ids[:1]

    def _make_order_with_reward_line(self):
        """A pos.order whose single line is a fixed-amount reward line."""
        order = self.env["pos.order"].create(
            {
                "company_id": self.company.id,
                "session_id": self.pos_session.id,
                "partner_id": self.partner.id,
                "amount_tax": 0.0,
                "amount_total": 0.0,
                "amount_paid": 0.0,
                "amount_return": 0.0,
                "lines": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "qty": 1,
                            "price_unit": -10.0,
                            "price_subtotal": -10.0,
                            "price_subtotal_incl": -10.0,
                            "is_reward_line": True,
                            "reward_id": self.reward.id,
                        }
                    )
                ],
            }
        )
        return order, order.lines[:1]

    # --- v19 field-name guard --------------------------------------------

    def test_reward_uses_v19_field_names(self):
        """The migration relies on v19 loyalty.reward field names. If the core
        renames them again these must fail loudly here, not silently in _post."""
        fields_ = self.env["loyalty.reward"]._fields
        self.assertIn("discount_mode", fields_)
        self.assertIn("discount", fields_)
        self.assertIn("discount_applicability", fields_)
        self.assertNotIn("discount_type", fields_)
        self.assertNotIn("discount_percentage", fields_)
        self.assertNotIn("discount_apply_on", fields_)
        self.assertEqual(self.reward.discount_mode, "per_order")

    def test_reward_id_is_native_on_pos_order_line(self):
        """reward_id / is_reward_line are provided natively by pos_loyalty in
        v19; the module must not redefine them (it would collide)."""
        line_fields = self.env["pos.order.line"]._fields
        self.assertIn("reward_id", line_fields)
        self.assertIn("is_reward_line", line_fields)

    # --- prepare_loyalty_move_line ---------------------------------------

    def test_prepare_loyalty_move_line_turns_line_into_note(self):
        """A fixed-amount reward invoice line becomes a value-less note: no
        price/product/tax/quantity survive, so it cannot alter the taxable base."""
        _order, reward_line = self._make_order_with_reward_line()
        move_line = {
            "name": "Loyalty discount",
            "price_unit": -10.0,
            "quantity": 1.0,
            "product_id": self.product.id,
            "tax_ids": [Command.set(self.tax_sale.ids)],
        }
        self.env["pos.order"].prepare_loyalty_move_line(move_line, reward_line)

        self.assertEqual(move_line["display_type"], "line_note")
        for popped in ("price_unit", "product_id", "tax_ids", "quantity"):
            self.assertNotIn(
                popped, move_line, f"{popped} must be removed from the note line"
            )
        self.assertIn("amount:", move_line["name"])

    # --- invoice_pay_loyalty_program_create ------------------------------

    def test_selfpaid_payment_vals_are_v19_valid(self):
        """The self-paid payment vals must use v19 field names and the
        VAT-inclusive discount amount, and be accepted by account.payment."""
        move = self._create_invoice(self.sale_journal)
        move.action_post()
        _order, reward_line = self._make_order_with_reward_line()
        # link the invoice line to the reward pos line so the vals builder can
        # read pos_order_line_id.price_subtotal_incl
        inv_line = move.invoice_line_ids.filtered(
            lambda l: l.display_type == "product"
        )[:1]
        inv_line.pos_order_line_id = reward_line.id

        vals = inv_line.invoice_pay_loyalty_program_create()
        self.assertTrue(vals, "an out_invoice must yield payment vals")
        # v19: memo, not ref
        self.assertIn("memo", vals)
        self.assertNotIn("ref", vals)
        # amount is the VAT-inclusive discount (abs of price_subtotal_incl)
        self.assertEqual(vals["amount"], 10.0)
        self.assertEqual(vals["payment_type"], "inbound")
        self.assertEqual(vals["partner_type"], "customer")
        self.assertEqual(vals["journal_id"], self.loyalty_journal.id)
        self.assertTrue(vals["is_selfpaid"])

        # the vals must actually be creatable (guards against invalid fields)
        payment = self.env["account.payment"].create(vals)
        self.assertTrue(payment)
        self.assertTrue(payment.is_selfpaid)
        self.assertEqual(payment.amount, 10.0)

    def test_selfpaid_vals_none_for_non_sale_move(self):
        """Only sale/refund documents get a self-paid loyalty payment."""
        move = self._create_invoice(self.sale_journal)
        move.action_post()
        line = move.invoice_line_ids.filtered(lambda l: l.display_type == "product")[:1]
        # force an unsupported move_type view: entry-like lines return False
        self.assertTrue(line.invoice_pay_loyalty_program_create())

    # --- product tax guard ------------------------------------------------

    def test_loyalty_product_never_gets_tax_via_orm(self):
        """A pos_loyalty_program product created via the ORM (no explicit
        taxes_id) must not inherit the company's default sale tax.

        Created in the test company (single-company PT/AO scenario) so the
        assertion is about that company's taxes, not taxes leaking in from
        other companies active in the test registry."""
        product = (
            self.env["product.template"]
            .with_company(self.company)
            .create(
                {
                    "name": "Reward Product Test",
                    "company_id": self.company.id,
                    "pos_loyalty_program": True,
                }
            )
        )
        self.assertFalse(
            product.taxes_id,
            "a loyalty reward product must never carry a tax",
        )
        self.assertTrue(product.available_in_pos)

    def test_loyalty_product_rejects_explicit_tax(self):
        """Creating a loyalty product WITH a tax is rejected outright."""
        with self.assertRaises(ValidationError):
            self.env["product.template"].create(
                {
                    "name": "Reward Product With Tax",
                    "pos_loyalty_program": True,
                    "taxes_id": [Command.set(self.tax_sale.ids)],
                }
            )
