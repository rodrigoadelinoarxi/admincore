from odoo import api,  fields, models


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    deferral_type = fields.Selection(related='account_depreciation_id.account_asset_type', store=True)
    account_depreciation_id_account_type = fields.Selection(related='account_depreciation_id.account_type', store=True)
    movement_type = fields.Selection(selection=[('debit', 'Debit'), ('credit', 'Credit')], default='credit')
