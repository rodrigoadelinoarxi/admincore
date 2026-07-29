from odoo import models, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    #
    # def open_pt_balance_report(self):
    #     return {
    #         'name': _('Balance'),
    #         'type': 'ir.actions.client',
    #         'tag': 'account_report',
    #         'params': {
    #             'options': {'analytic_accounts': [self.id]},
    #             'ignore_session': 'both',
    #         },
    #         'context': {
    #             'model': 'account.financial.html.report',
    #             'id': self.env.ref('l10n_pt_reports_arxi.account_financial_report_line_pt_balanco').id,
    #         }
    #     }
    #
    # def open_profit_and_loss_report(self):
    #     return {
    #         'name': _('Profit and Loss'),
    #         'type': 'ir.actions.client',
    #         'tag': 'account_report',
    #         'params': {
    #             'options': {'analytic_accounts': [self.id]},
    #             'ignore_session': 'both',
    #         },
    #         'context': {
    #             'model': 'account.financial.html.report',
    #             'id': self.env.ref('l10n_pt_reports_arxi.account_financial_report_l10n_pt_ddr').id,
    #         }
    #     }
