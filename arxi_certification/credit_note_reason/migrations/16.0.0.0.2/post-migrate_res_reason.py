from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.cr.execute("""SELECT *, name->>'en_US' AS name FROM res_reason;""")
    vals_list = []
    for r in env.cr.dictfetchall():
        vals_list.append({
            'name'    : r['name'],
            'sequence': r['sequence']
        })
    vals_list and env['account.move.refund.reason'].create(vals_list)
