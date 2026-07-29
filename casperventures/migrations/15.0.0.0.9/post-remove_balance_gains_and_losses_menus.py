from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    gains_and_losses_menu = env.ref('account_reports.account_financial_report_profitandloss0')
    gains_and_losses_menu.generated_menu_id.write({
        'active': False,
    })

    gains_and_losses_menu = env.ref('account_reports.account_financial_report_balancesheet0')
    gains_and_losses_menu.generated_menu_id.write({
        'active': False
    })
