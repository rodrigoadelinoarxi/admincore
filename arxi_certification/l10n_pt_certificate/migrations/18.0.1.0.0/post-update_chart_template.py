from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Update chart_template from 'pt_certificate' to 'pt_arxi' for Portuguese companies."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.company'].search([
        ('chart_template', '=', 'pt_certificate')
    ]).filtered(lambda c: c.country_id.code == 'PT').write({'chart_template': 'pt_arxi'})