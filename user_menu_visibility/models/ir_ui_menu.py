import logging
from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class IrActionReport(models.Model):
    _inherit = "ir.actions.report"
    _description = 'Ir Action Report'

    group_ids = fields.Many2many('res.groups', string='Groups Menu Visibility')
    users_ids = fields.Many2many('res.users', string='Users')
    protected = fields.Boolean("Protected", help="Make rule editable only for superuser")

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    @tools.ormcache('frozenset(self.env.user.group_ids.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        res = super(IrUiMenu, self)._visible_menu_ids(debug)
        return res - set(self.env.user.hidden_menu_ids.ids)

    @api.model
    def get_user_roots(self):
        menu_ids = super(IrUiMenu, self).get_user_roots()
        return menu_ids - self.env.user.hidden_menu_ids

    def _load_menus_blacklist(self):
        res = super()._load_menus_blacklist()
        if self.env.user.hidden_menu_ids:
            res += self.env.user.hidden_menu_ids.ids
        return res

    @api.model
    @tools.ormcache('self._uid', 'debug', 'self.env.context.get("lang")')
    def load_menus(self, debug):
        ir_act_report = self.env['ir.actions.report'].sudo().with_user(self.env.user).search(
            [('users_ids', '=', self.env.user.id), ('protected', '=', False)])
        ir_act_report1 = self.env['ir.actions.report'].sudo().with_user(self.env.user).search(
            [('users_ids', '!=', self.env.user.id), ('protected', '=', False)])
        if ir_act_report:
            ir_act_report.sudo().unlink_action()
        for report in ir_act_report1:
            try:
                report.sudo().create_action()
            except UserError as e:
                # alguns relatórios (ex.: Planning) recusam create_action() no
                # Odoo 19 e obrigam a usar o botão Imprimir da própria vista;
                # ignorar em vez de rebentar o load_menus para todos os users
                _logger.warning("create_action() recusado para o relatório '%s': %s", report.display_name, e)
        return super(IrUiMenu, self).load_menus(debug)
