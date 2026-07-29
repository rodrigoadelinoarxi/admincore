from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['sale.order'].search([('state', '=', 'draft')]).write({'name': '/'})
