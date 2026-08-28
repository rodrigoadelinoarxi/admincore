from odoo import models


class AccountTaxExemption(models.Model):
    _inherit = 'account.tax.exemption'

    # The deployed 'account.tax.exemption' model (l10n_pt_ao, pyarmor-obfuscated)
    # orders by 'display_name', a computed field that is NOT stored in this
    # build. Odoo 19 tightened _order_field_to_sql() to raise instead of
    # silently falling back when a non-stored field is used for ordering,
    # which crashed the upgrade.odoo.com crawl test on the "Tax Exemptions"
    # menu ('Cannot convert account.tax.exemption.display_name to SQL because
    # it is not stored'). 'code' is a required, indexed, stored field with
    # the same practical sort behaviour, so it's a safe replacement.
    _order = 'code'
