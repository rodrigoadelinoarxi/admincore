=====================
Portugal - Accounting
=====================

Portuguese Accounting and Invoicing
-----------------------------------

This module implements several Portuguese specific functionalities:

- Documents and their respective reports were updated:
    * Invoices
    * Payments
    * Debit Notes
    * Credit Notes
    * Suplier Debit Notes

* Certified Document Hashing

* Generation of a Standard Audit File for Tax (SAFT)

* Portuguese Chart of Accounts.

* Portuguese Taxes and Ecotaxes.

* Portuguese Fiscal Positions.

* Simplified invoices (Fatura Simplificada).

* Restricts importing invoices to certified journals.

* QR Code.

* ATCUD.

* Specific numbering sequences for different document type inside the same journal.

* Restricts editing values for taxes used in certified documents.

* Show exchange rate and document totals in both currencies for invoices in a foreign currency.

* SAF-T Import (Chart of Accounts, Taxes, Journals, Account Moves, Documents, Customers, Products).

* SAF-T Export (Invoicing, Accounting, Self-billing).

Webservice AT
-------------

To Extract the Test Certificates:

#. openssl pkcs12 -cacerts -nokeys -in TesteWebservices.pfx -out ca-cert.ca -password pass:TESTEwebservice -passin pass:TESTEwebservice
#. openssl pkcs12 -nocerts -in TesteWebservices.pfx -out private.key -password pass:TESTEwebservice -passin pass:TESTEwebservice -passout pass:TESTEwebservice
#. openssl rsa -in private.key -out "NewKeyFile.key" -passin pass:TESTEwebservice
#. cat "NewKeyFile.key" "certificate.crt" "ca-cert.ca" > PEM.pem
#. openssl pkcs12 -export -nodes -CAfile ca-cert.ca -in PEM.pem -out "test_certificate.pem"


Requirements (External Dependencies)
------------------------------------
- pycryptodome
- xmlschema
- pdftotext

>>> Ubuntu sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev

>>> pip3 install pycryptodome xmlschema pdftotext


Known Issues
------------
1. Multicompany compatibility

Missing Features
----------------
1. Withholding tax
2. Delivery slip
3. Consignment note
4. Accounting SAF-T document
