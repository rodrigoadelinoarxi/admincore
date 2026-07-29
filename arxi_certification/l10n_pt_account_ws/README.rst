License: `Odoo Proprietary License v1.0 <https://www.odoo.com/documentation/17.0/legal/licenses.html#odoo-apps>`_

Odoo Portuguese Invoicing External API
======================================

Adds several endpoints to be called by a webservice to create Portuguese certified documents.

Installation
------------

To install this module, you need to:

- Download the module
- Unzip to the addons path
- Install the module in Odoo Community or Enterprise

Response Codes
--------------

- 430 Missing required fields
- 431 Missing required fields for Invoice Lines
- 432 Invoice not found
- 433 Invoice not cancelled
- 434 Invalid refund option
- 435 Partner not found
- 436 Invoice not found

Callable Methods
----------------

### Create And Post Invoice

``create_and_post_pt_invoice``

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Required
     - Type
     - Example
   * - partner_vat
     - Partner VAT number as registered in Odoo (required if partner_id is empty)
     - **Yes**
     - string
     - "519999993"
   * - partner_id
     - Odoo Partner ID (required if partner_id is empty)
     - **Yes**
     - integer
     - 31
   * - journal_id
     - Odoo Journal ID where to register the invoice
     - *Yes*
     - integer
     - 1
   * - invoice_date
     - Invoice Date
     - No
     - date
     - 2020-01-01
   * - invoice_date_due
     - Invoice Due Date
     - No
     - date
     - 2020-01-31
   * - company_id
     - Odoo Company ID
     - No
     - integer
     - 1
   * - lines
     - Invoice Lines
     - *Yes*
     - list
     - [{'product_id': 15, 'quantity': 2, 'price_unit': 850.02}]
   * - extra_values
     - Extra values to be used when creating the invoice
     - No
     - dict
     - {"payment_reference": "example_reference"}

Lines

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Required
     - Type
     - Example
   * - product_id
     - Odoo Product ID
     - *Yes*
     - integer
     - 52
   * - quantity
     - Quantity
     - *Yes*
     - float
     - 2
   * - price_unit
     - Price Unit
     - No
     - float
     - 13.50
   * - discount
     - Discount
     - No
     - float
     - 20
   * - tax_ids
     - Tax Ids
     - No
     - list
     - [1]

### Pay Invoice

``pay_pt_invoice``

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Required
     - Type
     - Example
   * - number
     - Invoice number (required if invoice_id is empty)
     - **Yes**
     - string
     - "FT 2020/0001"
   * - invoice_id
     - Odoo Invoice ID (required if number is empty)
     - **Yes**
     - integer
     - 5
   * - company_id
     - Odoo Company ID
     - No
     - integer
     - 1
   * - payment_mechanism_code
     - Payment Mechanism Code
     - No
     - string
     - "TB"
   * - payment_mechanism_id
     - Payment Mechanism ID
     - No
     - integer
     - 1

### Cancel Invoice

``cancel_pt_invoice``

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Required
     - Type
     - Example
   * - number
     - Invoice number (required if invoice_id is empty)
     - **Yes**
     - string
     - "FT 2020/0001"
   * - invoice_id
     - Odoo Invoice ID (required if number is empty)
     - **Yes**
     - integer
     - 5
   * - reason
     - Reason for the invoice cancel
     - No
     - string
     - "Customer declined the products"
   * - company_id
     - Odoo Company ID
     - No
     - integer
     - 1

### Add Credit Note

``create_pt_credit_note``

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Required
     - Type
     - Example
   * - number
     - Invoice number (required if invoice_id is empty)
     - **Yes**
     - string
     - "FT 2020/0001"
   * - invoice_id
     - Odoo Invoice ID (required if number is empty)
     - **Yes**
     - integer
     - 5
   * - reason
     - Reason for the invoice credit note
     - No
     - string
     - "Customer declined the products"
   * - refund_method
     - Type of refund method (refund, cancel, modify)
     - No
     - string
     - "refund"
   * - company_id
     - Odoo Company ID
     - No
     - integer
     - 1

Refund Methods
--------------

* **refund** - creates a draft credit note.
* **cancel** - creates, posts and reconciles the credit note with the invoice.
* **modify** - same as cancel but creates a new draft invoice with the same data as the original invoice.

Example
-------

.. code:: python

     import xmlrpc.client

     # Test Env
     url = 'https://localhost:8069'
     db = 'test_database'
     username = 'adminusername'
     password = 'admintoken'

     # Base env
     models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
     common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
     uid = common.authenticate(db, username, password, {})

     # Get Sale Journal #
     journal_id = models.execute_kw(db, uid, password, 'account.journal', 'search', [[['type', '=', 'sale']]], {'limit': 1})
     journal_id = journal_id and journal_id[0]

     tax_id = models.execute_kw(db, uid, password, 'account.tax', 'search', [[['type_tax_use', '=', 'sale'], ['amount', '=', 6]]], {'limit': 1})
     tax_id = tax_id and tax_id[0]

     values = {
     'partner_vat': '216422736',
     'journal_id': 8,
     'invoice_date': '2020-12-18',
     'invoice_date_due': '2020-12-18',
     'lines': [{'product_id': 15, 'quantity': 2, 'price_unit': 850.02, 'tax_ids': [tax_id]}],
     'extra_values': {'payment_reference': "REF55"}
     }
     print(models.execute_kw(db, uid, password, 'account.move', 'create_and_post_pt_invoice', [values]))


License
-------

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
