from odoo import models, _
from odoo.exceptions import UserError


class AccountBatchPayment(models.Model):
    _inherit = 'account.batch.payment'

    def write(self, vals):
        # Guardar pagamentos antes da alteração
        old_payment_map = {batch.id: set(batch.payment_ids.ids) for batch in self}

        res = super().write(vals)

        for batch in self:
            old_ids = old_payment_map.get(batch.id, set())
            new_ids = set(batch.payment_ids.ids)

            removed_ids = old_ids - new_ids
            if removed_ids:
                removed_payments = self.env['account.payment'].browse(removed_ids).filtered(
                    lambda p: p.state not in ('cancel', 'draft')
                )
                if removed_payments:
                    try:
                        removed_payments.action_cancel()
                    except Exception:
                        raise UserError(_("Não foi possível cancelar alguns pagamentos removidos do lote."))

        return res
