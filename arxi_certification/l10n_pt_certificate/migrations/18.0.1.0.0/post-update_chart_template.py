from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Update chart_template from 'pt_certificate' to 'pt_arxi' for Portuguese companies."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.company'].search([
        ('country_id.code', '=', 'PT'),
        ('chart_template', '=', 'pt_certificate')
    ]).write({'chart_template': 'pt_arxi'})