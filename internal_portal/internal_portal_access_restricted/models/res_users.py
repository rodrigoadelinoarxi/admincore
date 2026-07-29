from odoo import SUPERUSER_ID, _, api, models
from odoo.exceptions import AccessError

from odoo.addons.base.models.res_users import is_reified_group

IR_CONFIG_NAME = "access_restricted.fields_view_get_uid"


class ResGroups(models.Model):
    _inherit = "res.groups"

    @api.model
    def get_application_groups(self, domain):

        # ACCOUNT
        group_account_user = self.env.ref('account.group_account_user', raise_if_not_found=False)
        if group_account_user and group_account_user.category_id.xml_id == 'base.module_category_hidden':
            domain += [('id', '!=', group_account_user.id)]
        group_account_readonly = self.env.ref('account.group_account_readonly', raise_if_not_found=False)
        if group_account_readonly and group_account_readonly.category_id.xml_id == 'base.module_category_hidden':
            domain += [('id', '!=', group_account_readonly.id)]

        # BASE + INTERNAL PORTAL
        categ_id = self.env.ref('base_internal_portal.module_category_internal_portal')
        return self.search(domain + [('share', '=', False), ('category_id', '!=', categ_id.id)])
