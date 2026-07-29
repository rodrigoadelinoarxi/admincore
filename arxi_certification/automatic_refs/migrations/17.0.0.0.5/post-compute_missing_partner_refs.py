import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if env['ir.config_parameter'].sudo().get_param('automatic_refs.partner_ref_type') == '1':
        partners = env['res.partner'].search([('ref', '=', False),  ('active', 'in', (True, False))])
        for partner in partners:
            partner.ref = env['res.partner'].get_next_available_customer_ref()
            _logger.info('Partner %s has been assigned the reference %s', partner.name, partner.ref)
