import logging
from lxml import etree
from lxml.builder import E
from collections import defaultdict

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG

_logger = logging.getLogger(__name__)

def name_selection_groups(ids):
    return 'sel_groups_' + '_'.join(str(it) for it in sorted(ids))


def name_boolean_group(id):
    return 'in_group_' + str(id)


class GroupsView(models.Model):
    _inherit = 'res.groups'

    def get_application_groups(self, domain):
        """ Return the non-share groups that satisfy ``domain``. """
        domain.append(('category_id', '!=', self.env.ref('base_internal_portal.module_category_internal_portal').id))
        return super(GroupsView, self).get_application_groups(domain)

    def get_portal_groups_to_view(self):
        """ Return all groups classified by application (module category), as a list::

                        [(app, kind, groups), ...],

                    where ``app`` and ``groups`` are recordsets, and ``kind`` is either
                    ``'boolean'`` or ``'selection'``. Applications are given in sequence
                    order.  If ``kind`` is ``'selection'``, ``groups`` are given in
                    reverse implication order.
                """

        def linearize(app, gs, category_name):
            order = {g: len(g.trans_implied_ids & gs) for g in gs}
            return (app, 'boolean', gs, (100, 'Other'))

        # classify all groups by application
        by_app, others = defaultdict(self.browse), self.browse()
        categ_id = self.env.ref('base_internal_portal.module_category_internal_portal')
        groups = self.search([('category_id', '=', categ_id.id)])
        for g in groups:
            by_app[categ_id] += g
        # build the result
        res = []
        for app, gs in sorted(by_app.items(), key=lambda it: it[0].sequence or 0):
            # if app.parent_id:
            #     res.append(linearize(app, gs, (app.parent_id.sequence, app.parent_id.name)))
            # else:
            res.append(linearize(app, gs, (100, 'Other')))

        return res

    @api.model
    def _update_user_groups_view(self):
        res = super(GroupsView, self)._update_user_groups_view()

        self = self.with_context(lang=None)
        view = self.env.ref('base_internal_portal.view_users_form_inherit_groups', raise_if_not_found=False)
        if not (view and view.exists() and view._name == 'ir.ui.view'):
            return
        if self._context.get('install_filename') or self._context.get(MODULE_UNINSTALL_FLAG):
            # use a dummy view during install/upgrade/uninstall
            xml = E.page(name='access_rights', position="inside")
        else:
            xml1 = []
            xml1.append(E.separator(string='Internal Portal', colspan="2", groups='base.group_no_one'))
            sorted_tuples = sorted(self.get_portal_groups_to_view(),
                                   key=lambda t: t[0].xml_id != 'base.module_category_user_type')
            for app, kind, gs, category_name in sorted_tuples:
                if app.xml_id == 'base_internal_portal.module_category_internal_portal':
                    for g in gs:
                        field_name = name_boolean_group(g.id)
                        # xml1.append(E.field(name=field_name, **attrs))
                        xml1.append(E.field(name=field_name))
                        xml1.append(E.newline())

            xml = E.page(E.group(*(xml1), col="2"), name='access_rights', position="inside")
            xml.addprevious(etree.Comment("GENERATED AUTOMATICALLY BY GROUPS"))

        xml_content = etree.tostring(xml, pretty_print=True, encoding="unicode")
        if xml_content != view.arch:  # avoid useless xml validation if no change
            new_context = dict(view._context)
            new_context.pop('install_filename', None)  # don't set arch_fs for this computed view
            new_context['lang'] = None
            view.with_context(new_context).write({'arch': xml_content})
        return res
