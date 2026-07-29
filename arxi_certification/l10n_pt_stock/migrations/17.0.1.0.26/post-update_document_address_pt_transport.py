from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    pt_transport = env['pt.transport'].search([('state', '!=', 'draft')])

    for rec in pt_transport:
        if rec.document_address_id:
            rec.document_address_id.vat = rec.partner_id.vat
        else:
            rec.save_address()