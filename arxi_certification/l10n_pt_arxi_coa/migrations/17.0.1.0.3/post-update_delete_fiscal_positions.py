from odoo import SUPERUSER_ID, api
import logging

_logger = logging.getLogger(__name__)

IDS = ['withholding_25_rental', 'withholding_25_rental_irc', 'withholding_11_5', 'withholding_16_5', 'withholding_20', 'withholding_25']


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for company in env['res.company'].search([]):
        for id in IDS:
            if fiscal_position := env.ref(f"account.{company.id}_{id}", raise_if_not_found=False):
                fiscal_position.unlink()

