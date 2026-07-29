from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    account_move = env['account.move'].search([('document_address_id', '!=', False), ('state', '!=', 'draft')])

    for rec in account_move:
        rec.document_address_id.vat = rec.partner_id.vat

    account_payment = env['account.payment'].search([('state', '!=', 'draft')])

    for rec in account_payment:
        if rec.document_address_id:
            rec.document_address_id.vat = rec.partner_id.vat
        else:
            rec.save_address()
