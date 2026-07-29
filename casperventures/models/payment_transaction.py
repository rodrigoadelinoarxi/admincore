from odoo import models, fields


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'


    def _finalize_post_processing(self):
        return super(PaymentTransaction, self.with_context(payment_transaction=True))._finalize_post_processing()
