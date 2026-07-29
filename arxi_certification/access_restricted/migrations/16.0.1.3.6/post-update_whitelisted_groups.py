from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    whitelisted_group_ids = env['res.groups'].get_default_whitelisted_groups()
    whitelisted_group_ids.write({
        'whitelisted_group': True
    })
