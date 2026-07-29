from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for company_id in env['res.company'].search([]):
        # Adds sale journals for the new sale types
        for sale_type in env['sale.order.type'].search([('code', 'in', ['OU'])]):
            if not env['sale.order.journal'].search_count(
                    [('name', '=', sale_type.name), ('sale_type_id', '=', sale_type.id), ('company_id', '=', company_id.id)]):
                vals = {
                    'name'        : sale_type.name,
                    'prefix'      : '',
                    'sale_type_id': sale_type.id,
                    'company_id'  : company_id.id,
                }
                env['sale.order.journal'].create(vals)
