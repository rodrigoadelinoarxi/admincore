License: [Odoo Proprietary License v1.0](https://www.odoo.com/documentation/17.0/legal/licenses.html#odoo-apps)

# Portugal - E-Invoicing (CIUS-PT)

Creates CIUS-PT Eletronic XMl document for invoice

## Installation

To install this module, you need to:

- Download the module
- Unzip to the addons path
- Install the module in Odoo Community or Enterprise

## Testing

Use this to update the partner / company in the console so the PT company has the vat you insert
``` sql
update res_partner set vat='' where id=42;
```

## Odoo Eletronic Data Interchange (EDI)

Odoo uses account.edi.format to implement EDI with several functions ready to reimplement:

### Indicate if this EDI must be generated for the invoice passed as parameter
* invoice: An account.move having the invoice type
* Returns: True if the EDI must be generated, False otherwise
```python3
def _is_required_for_invoice(self, invoice):
    # OVERRIDE
    self.ensure_one()
    if self.code != 'cius_pt':
        return super()._is_required_for_invoice(invoice)
    # VALIDATIONS
    return True
```

### Indicate if this EDI must be generated for the payment passed as parameter
* move: An account.move linked to either an account.payment, either an account.bank.statement.line
* Returns: True if the EDI must be generated, False otherwise
```python3
def _is_required_for_payment(self, move):
    # OVERRIDE
    self.ensure_one()
    if self.code != 'cius_pt':
        return super()._is_required_for_payment(move)

    # VALIDATIONS
    if move.country_code != 'PT':
        return False
    
    return True
```

### Indicate if the EDI must be generated asynchronously through to some web services
* Returns: True if such a web service is available, False otherwise
```python3
def _needs_web_services(self):
    # OVERRIDE
    return self.code == 'cius_pt' or super()._needs_web_services()
```

### Indicate if the EDI format should appear on the journal passed as parameter to be selected by the user. If True, this EDI format will be selected by default on the journal
* journal: The journal
* Returns: True if this format can be enabled by default on the journal, False otherwise
```python3
def _is_compatible_with_journal(self, journal):
    # OVERRIDE
    self.ensure_one()
    if self.code != 'cius_pt':
        return super()._is_compatible_with_journal(journal)
    return journal.type == 'sale' and journal.country_code == 'PT'
```

### Indicate if the EDI must be embedded inside the PDF report
* Returns: True if the documents need to be embedded, False otherwise
```python3
def _is_embedding_to_invoice_pdf_needed(self):
    # OVERRIDE
    self.ensure_one()
    return True if self.code == 'cius_pt' else super()._is_embedding_to_invoice_pdf_needed()
```

### Get the values to embed to pdf
- Returns: A dictionary {'name': name, 'datas': datas} or False if there are no values to embed
  - name: The name of the file
  - datas: The bytes ot the file
```python3
def _get_embedding_to_invoice_pdf_values(self, invoice):
    # OVERRIDE
    values = super()._get_embedding_to_invoice_pdf_values(invoice)
    if values and self.code == 'cius_pt':
        values['name'] = 'cius_pt.xml'
    return values
```

### Indicate if we can send multiple documents in the same time to the web services. If True, the \_post_%s_edi methods will get multiple documents in the same time. Otherwise, these methods will be called with only one record at a time
* Returns: True if batching is supported, False otherwise
```python3
def _support_batching(self, move=None, state=None, company=None):
    # OVERRIDE
    if self.code == 'cius_pt':
        return state == 'to_cancel' and move.is_invoice()
    
    return super()._support_batching(move=move, state=state, company=company)
```

### Returns a tuple that will be used as key to partitionnate the invoices/payments when creating batches with multiple invoices/payments. The type of move (invoice or payment), its company_id, its edi state and the edi_format are used by default, if no further partition is needed for this format, this method should return ()
* Returns: The key to be used when partitionning the batches.
```python3
def _get_batch_key(self, move, state):
    # OVERRIDE
    if self.code == 'cius_pt' and state == 'to_cancel':
        return (move.l10n_pe_edi_cancel_cdr_number,)
    return super()._get_batch_key(move, state)
```

### Checks the move and relevant records for potential error (missing data, etc)
* move: The move to check
* Returns: A list of error messages
```python3
def _check_move_configuration(self, move):
    # OVERRIDE
    res = super()._check_move_configuration(move)
    if self.code != 'cius_pt':
        return res
    
    # APPEND ERROR TO ERROR LIST(res)
    if not move.company_id.vat:
        res.append("VAT number is missing on company %s" % move.company_id.display_name)
    
    return res
```

### Create the file content representing the invoice (and calls web services if necessary)
- invoices: A list of invoices to post
- test_mode: A flag indicating the EDI should only simulate the EDI without sending data
- Returns: A dictionary with the invoice as key and as value, another dictionary:
  - attachment: The attachment representing the invoice in this edi_format if the edi was successfully posted
  - error: An error if the edi was not successfully posted
  - blocking_level: (optional, requires account_edi_extended) How bad is the error (how should the edi flow be blocked ?)
```python3
def _post_invoice_edi(self, invoices, test_mode=False):
    # OVERRIDE
    edi_result = super()._post_invoice_edi(invoices, test_mode=test_mode)
    if self.code != 'cius_pt':
        return edi_result

    for invoice in invoices:
        # == Check the configuration ==
        errors = self._l10n_pt_edi_check_configuration(invoice)
        if errors:
            edi_result[invoice] = {
                'error': self._l10n_pt_edi_format_error_message("Invalid configuration:", errors),
            }
            continue
        
        # == Generate the CIUS-PT ==
        res = self._l10n_pt_edi_export_invoice_cius_pt(invoice)

        # == Call the web-service, test_mode parameter for test ==
        if test_mode:
            res['cius_signed'] = res['cius_str']
            res['cius_encoding'] = 'str'
        else:
            res = self._make_web_service_call_post_invoice()
        
        # == Create the attachment ==
        cius_pt_attachment = self._create_invoice_cius_pt_attachment(invoice, res['cius_pt_signed'])
        edi_result[invoice] = {'attachment': cius_pt_attachment}

        # == Chatter ==
        invoice.with_context(no_new_invoice=True).message_post(
            body="The CIUS-PT document was successfully created and signed by the government.",
            attachment_ids=cius_pt_attachment.ids,
        )
    return edi_result
```

### Calls the web services to cancel the invoice of this document.
- invoices: A list of invoices to cancel
- test_mode: A flag indicating the EDI should only simulate the EDI without sending data
- Returns: A dictionary with the invoice as key and as value, another dictionary:
  - success: True if the invoice was successfully cancelled
  - error: An error if the edi was not successfully cancelled
  - blocking_level: (optional, requires account_edi_extended) How bad is the error (how should the edi flow be blocked ?)
```python3
def _cancel_invoice_edi(self, invoices, test_mode=False):
    # OVERRIDE
    edi_result = super()._cancel_invoice_edi(invoices, test_mode=test_mode)
    if self.code != 'cius_pt':
        return edi_result

    for invoice in invoices:
        # == Check the configuration ==
        errors = self._l10n_pt_edi_check_configuration(invoice)
        if errors:
            edi_result[invoice] = {
                'error': self._l10n_pt_edi_format_error_message("Invalid configuration:", errors)
            }
            continue

        # == Call the web-service, test_mode parameter for test ==
        if test_mode:
            res = {'success': True}
        else:
            res = self._make_web_service_call_cancel_invoice()

        edi_result[invoice] = res

        # == Chatter ==
        invoice.with_context(no_new_invoice=True).message_post(
            body="The CIUS-PT document has been successfully cancelled.",
            subtype_xmlid='account.mt_invoice_validated',
        )

    return edi_result
```

### Create the file content representing the payment (and calls web services if necessary)
- payments: The payments to post
- test_mode: A flag indicating the EDI should only simulate the EDI without sending data
- Returns: A dictionary with the payment as key and as value, another dictionary:
  - attachment: The attachment representing the payment in this edi_format if the edi was successfully posted
  - error: An error if the edi was not successfully posted
  - blocking_level: (optional, requires account_edi_extended) How bad is the error (how should the edi flow be blocked ?)
```python3
def _post_payment_edi(self, payments, test_mode=False):
    # OVERRIDE
    edi_result = super()._post_payment_edi(payments, test_mode=test_mode)
    if self.code != 'cius_pt':
        return edi_result

    for move in payments:
        # == Check the configuration ==
        errors = self._l10n_pt_edi_check_configuration(move)
        if errors:
            edi_result[move] = {
                'error': self._l10n_pt_edi_format_error_message("Invalid configuration:", errors),
            }
            continue

        # == Generate the CIUS-PT ==
        res = self._l10n_pt_edi_export_payment_cius_pt(move)

        # == Call the web-service, test_mode parameter for test ==
        if test_mode:
            res['cius_signed'] = res['cius_str']
            res['cius_encoding'] = 'str'
        else:
            res = self._make_web_service_call_post_payment()

        # == Create the attachment ==
        cius_pt_attachment = self._create_payment_cius_pt_attachment(move, res['cius_signed'])
        edi_result[move] = {'attachment': cius_pt_attachment}

        # == Chatter ==
        message = "The CIUS-PT document has been successfully signed."
        move.message_post(body=message, attachment_ids=cius_pt_attachment.ids)
        if move.payment_id:
            move.payment_id.message_post(body=message, attachment_ids=cius_pt_attachment.ids)

    return edi_result
```

### Calls the web services to cancel the payment of this document
- payments: A list of payments to cancel
- test_mode: A flag indicating the EDI should only simulate the EDI without sending data
- Returns: A dictionary with the payment as key and as value, another dictionary:
  - success: True if the payment was successfully cancelled
  - error: An error if the edi was not successfully cancelled
  - blocking_level: (optional, requires account_edi_extended) How bad is the error (how should the edi flow be blocked ?)
```python3
def _cancel_payment_edi(self, payments, test_mode=False):
    # OVERRIDE
    edi_result = super()._cancel_payment_edi(payments, test_mode=test_mode)
    if self.code != 'cius_pt':
        return edi_result

    for move in payments:
        # == Check the configuration ==
        errors = self._l10n_pt_edi_check_configuration(move)
        if errors:
            edi_result[move] = {
                'error': self._l10n_pt_edi_format_error_message("Invalid configuration:", errors)
            }
            continue

        # == Call the web-service, test_mode parameter for test ==
        if test_mode:
            res = {'success': True}
        else:
            res = self._make_web_service_call_cancel_payment()

        edi_result[move] = res

        # == Chatter ==
        message = "The CIUS-PT document has been successfully cancelled."
        move.message_post(body=message)
        if move.payment_id:
            move.payment_id.message_post(body=message)

    return edi_result
```

## License

Odoo Proprietary License v1.0

This software and associated files (the "Software") may only be used (executed, modified, executed after modifications)
if you have purchased a valid license from the authors, typically via Odoo Apps, or if you have received a written
agreement from the authors of the Software (see the COPYRIGHT file).

You may develop Odoo modules that use the Software as a library (typically by depending on it, importing it and using
its resources), but without copying any source code or material from the Software. You may distribute those modules
under the license of your choice, provided that this license is compatible with the terms of the Odoo Proprietary
License (For example: LGPL, MIT, or proprietary licenses similar to this one).

It is forbidden to publish, distribute, sublicense, or sell copies of the Software or modified copies of the Software.

The above copyright notice and this permission notice must be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
