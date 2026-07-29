from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    sale_order = env['sale.order'].search([('document_address_id', '!=', False), ('state', '!=', 'draft')])

    for rec in sale_order:
        rec.document_address_id.vat = rec.partner_id.vat
