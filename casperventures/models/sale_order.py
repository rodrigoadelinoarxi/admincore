from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from markupsafe import Markup

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        self.ensure_one()
        vals = super(SaleOrder, self)._prepare_invoice()
        if self.sale_journal.default_invoice_journal:
            vals['journal_id'] = (self.sale_journal
                                  .default_invoice_journal and self.sale_journal.default_invoice_journal.id)
        return vals

    def action_quotation_sent(self):
        res = super(SaleOrder, self).action_quotation_sent()

        if self.company_id.id != 7: # 7 - Brainr S.A.
            return res

        template = self.env.ref('sale.email_template_edi_sale', raise_if_not_found=False)

        if template:
            template.send_mail(self.id, force_send=True)

            self.message_post(
                body=Markup(
                    f"📧 Quotation email sent to "
                    f"<b>{self.partner_id.email or 'unknown email'}</b> "
                    f"using template <b>{template.name}</b>."
                ),
                message_type="comment",
                subtype_xmlid="mail.mt_note",
            )

        return res


