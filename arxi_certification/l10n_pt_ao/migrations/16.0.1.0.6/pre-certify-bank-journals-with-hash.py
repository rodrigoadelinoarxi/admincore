from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cr.execute(
        "UPDATE account_journal SET restrict_mode_hash_table = True where type in ('bank', 'cash') AND l10n_cert = True")
    for rec in env['account.journal'].search([
        ('restrict_mode_hash_table', '=', True),
        ('secure_sequence_id', '=', False)
    ]):
        rec._create_secure_sequence(['secure_sequence_id'])
