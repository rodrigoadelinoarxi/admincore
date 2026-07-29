from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for move in env['account.move'].search([('country_code', 'in', ['PT', 'AO']), ('move_type', 'in', ['in_refund', 'out_refund'])]):
        if move.move_type == 'in_refund':
            move.tax_report_refund_type_supplier = move.tax_report_refund_type
        elif move.move_type == 'out_refund':
            move.tax_report_refund_type_customer = move.tax_report_refund_type