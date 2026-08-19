from odoo import _, models, Command
from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_repr
from odoo.tools.float_utils import float_round
from odoo.tools.misc import formatLang
from odoo.tools.zeep import Client
import logging
_logger = logging.getLogger(__name__)

class AccountEdiCommonInherit(models.AbstractModel):
    _inherit = "account.edi.common"

    def _import_invoice_ubl_cii(self, invoice, file_data, new=False):
        """
        Override `_import_invoice_ubl_cii` to prevent duplicate processing of embedded XML files.
        """
        _logger.info("passa_aqui")
        # Call the original method first
        super()._import_invoice_ubl_cii(invoice, file_data, new)

        tree = file_data['xml_tree']

        # Prevent multiple XML processing
        additional_docs = tree.findall('./{*}AdditionalDocumentReference')

        processed = False  # Flag to prevent handling multiple XMLs

        for document in additional_docs:
            if processed:  # If already processed, stop
                break

            attachment_name = document.find('{*}ID')
            attachment_data = document.find('{*}Attachment/{*}EmbeddedDocumentBinaryObject')

            if attachment_name is not None \
                    and attachment_data is not None \
                    and attachment_data.attrib.get('mimeCode') == 'application/pdf':
                text = attachment_data.text
                name = (attachment_name.text or 'invoice').split('\\')[-1].split('/')[-1].split('.')[0] + '.pdf'

                # Prevent duplicate invoice creation
                existing_invoice = self.env['account.move'].search([
                    ('message_main_attachment_id.name', '=', name),
                    ('move_type', '=', invoice.move_type),
                    ('partner_id', '=', invoice.partner_id.id),
                ], limit=1)

                if existing_invoice:
                    continue  # Skip duplicate invoice processing

                self.env['ir.attachment'].create({
                    'name': name,
                    'res_id': invoice.id,
                    'res_model': 'account.move',
                    'datas': text + '=' * (len(text) % 3),  # Fix incorrect padding
                    'type': 'binary',
                    'mimetype': 'application/pdf',
                })

                processed = True  # Mark as processed to prevent handling multiple embedded XMLs
