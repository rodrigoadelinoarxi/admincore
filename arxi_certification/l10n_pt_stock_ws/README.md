License: [Odoo Proprietary License v1.0](https://www.odoo.com/documentation/17.0/legal/licenses.html#odoo-apps)

# Odoo Portuguese Transport External API

Adds several endpoints to be called by a webservice to create portuguese certified documents.

## Installation

To install this module, you need to:

- Download the module
- Unzip to the addons path
- Install the module in Odoo Community or Enterprise

## Response Codes

* 430 - Missing required fields
* 431 - Missing required fields for Transport Document Lines
* 432 - Transport Document not found
* 433 - Transport Document not cancelled
* 435 - Partner not found
* 436 - Transport Document not found
* 437 - AT Code error
* 438 - Empty delivery street field for partner
* 439 - Empty delivery city field for partner
* 440 - Empty delivery zip code field for partner

## Callable Methods

### Create And Post Transport Document

create_and_post_pt_transport

| Parameter                | Description                                                                | Required | Type     | Example                                                   |
| :---                     | :---                                                                       |  :----:  | :---     | :---                                                      |
| partner_vat              | Partner VAT number as registered in Odoo (required if partner_id is empty) | **       | string   | "519999993"                                               |
| partner_id               | Odoo Partner ID (required if partner_id is empty)                          | **       | integer  | 31                                                        |
| journal_id               | Odoo Journal ID where to register the transport                            | *        | integer  | 1                                                         |
| date                     | Document Posting Date                                                      |          | date     | 2020-01-01                                                |
| movement_start_date      | Movement Start Date                                                        | *        | datetime | 2020-01-31 12:00:00                                       |
| movement_end_date        | Movement End Date                                                          |          | datetime | 2020-01-31 14:00:00                                       |
| vehicle_id               | Vehicle License plate                                                      |          | string   | 01-AA-01                                                  |
| delivery_address_street  | Delivery Address Street (required if partner has an empty street field)    | **       | string   | Rua Capitão Henrique Galvão 46                            |
| delivery_address_city    | Delivery Address City (required if partner has an empty city field)        | **       | string   | Lisboa                                                    |
| delivery_address_zip     | Delivery Address Zip (required if partner has an empty zip code field)     | **       | string   | 1200-001                                                  |
| loading_address_street   | Loading Address Street                                                     |          | string   | Rua Prof. Zé Carlos 42                                    |
| loading_address_city     | Loading Address City                                                       |          | string   | Amadora                                                   |
| loading_address_zip      | Loading Address Zip                                                        |          | string   | 1100-001                                                  |
| company_id               | Odoo Company ID                                                            |          | integer  | 1                                                         |
| lines                    | Transport Document Lines                                                   | *        | list     | [{'product_id': 15, 'product_uom_qty': 2]                 |
| extra_values             | Extra values to be used when creating the transport document               |          | dict     | {"payment_reference": "example_reference"}                |

Lines

| Parameter  | Description     | Required | Type    | Example |
| :---       | :---            |  :----:  | :---    | :---    |
| product_id | Odoo Product ID | *        | integer | 52      |
| quantity   | Quantity        | *        | float   | 2       |

### Get Transport AT Code

get_transport_at_code

| Parameter    | Description                                          | Required | Type    | Example                          |
| :---         | :---                                                 |  :----:  | :---    | :---                             |
| number       | Transport number (required if transport_id is empty) | **       | string  | "GT 2020/0001"                   |
| transport_id | Odoo Transport ID (required if number is empty)      | **       | integer | 5                                |

### Cancel Transport

cancel_pt_transport

| Parameter    | Description                                          | Required | Type    | Example                          |
| :---         | :---                                                 |  :----:  | :---    | :---                             |
| number       | Transport number (required if transport_id is empty) | **       | string  | "GT 2020/0001"                   |
| transport_id | Odoo Transport ID (required if number is empty)      | **       | integer | 5                                |
| reason       | Reason for the transport cancel                      |          | string  | "Customer declined the products" |
| company_id   | Odoo Company ID                                      |          | integer | 1                                |

### Example

```python
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
# Get Transport Journal
journal_id = models.execute_kw(db, uid, password, 'pt.transport.journal', 'search', [[['movement_type', '=', 'transport.document']]], {'limit': 1})
journal_id = journal_id and journal_id[0]
# Transport Values
values = {
'partner_vat'        : '216422736',
'journal_id'         : journal_id,
'date'               : '2021-08-23',
'movement_start_date': '2021-08-23 12:00:00',
'movement_end_date'  : '2021-08-23 14:00:00',
'vehicle_id'        : '01-01-AA',
'lines'              : [{'product_id': 15, 'product_uom_qty': 2}],
}
print(models.execute_kw(db, uid, password, 'pt.transport', 'create_and_post_pt_transport', [values]))
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
