from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    proforma_group = env.ref('sale.group_proforma_sales', raise_if_not_found=False)
    if not proforma_group:
        return

    action_ids = [
        rec.id
        for rec in (
            env.ref('l10n_pt_ao_sale.convert_to_proforma', raise_if_not_found=False),
            env.ref('l10n_pt_ao_sale.duplicate_to_proforma', raise_if_not_found=False),
        )
        if rec
    ]
    if action_ids:
        env['ir.actions.server'].browse(action_ids).write({'group_ids': [(6, 0, proforma_group.ids)]})
