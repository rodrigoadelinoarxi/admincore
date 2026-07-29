import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    cr.execute(
        """ALTER TABLE product_product DROP CONSTRAINT product_product_code_uniq;""")
