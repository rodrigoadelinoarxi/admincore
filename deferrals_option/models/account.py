from odoo import api, models, fields


class AccountAccount(models.Model):
    _inherit = 'account.account'

    account_asset_type = fields.Selection(selection=[('expense', 'Expense'), ('revenue', 'Revenue')],
                                     compute="_check_account_asset_type", store=True, copy=False)

    @api.depends('account_type')
    def _check_account_asset_type(self):
        for rec in self:
            if rec.code.startswith('28'):
                rec.account_asset_type = 'expense'
            elif rec.code.startswith('272'):
                rec.account_asset_type = 'revenue'
            else:
                rec.account_asset_type = False

    @api.depends('account_type')
    def _compute_can_create_asset(self):
        """
            Adds asset_current and liability_current to the rec of assets that can create assets
        """
        super(AccountAccount, self)._compute_can_create_asset()

        for record in self:
            record.can_create_asset = record.account_type in ('asset_fixed', 'asset_non_current', 'asset_current',
                                                              'liability_current')

