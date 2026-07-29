import logging
_logger = logging.getLogger(__name__)

# from odoo.addons.product_sale_history.scripts.script_send_invite import create_portal_users
def create_portal_users(self):
    portal_wizard = self.env['portal.wizard'].sudo().create({})

    partner_list = self.env['res.partner'].search([('category_id', 'in', [self.env.ref('product_sale_history.res_partner_category_exclusive_sale').id])])
    counter_send = counter_error = counter_already_portal = 0
    list_error = []
    for partner_id in partner_list.filtered(lambda x: x.sale_order_ids.filtered(lambda y: y.state != 'draft')):
        if not self.env['res.users'].search([('login', '=', partner_id.email)]):
            portal_user_wizard = self.env['portal.wizard.user'].sudo().create({
                'partner_id': partner_id.id,
                'email'     : partner_id.email,
                'is_portal' : True,
                'wizard_id' : portal_wizard.id
            })
            try:
                portal_user_wizard.action_grant_access()
                if mail_template := self.env.ref('portal.mail_template_data_portal_welcome'):
                    lang = portal_user_wizard.user_id.lang

                    portal_url = partner_id.with_context(lang=lang)._get_signup_url_for_action()[partner_id.id]
                    mail_template.with_context(portal_url=portal_url, lang=lang).send_mail(portal_user_wizard.id)
                    counter_send += 1
            except Exception as e:
                _logger.info(f'Error creating portal user for {partner_id.name}\nError: {e}')
                counter_error += 1
                list_error.append({
                    'id'            : partner_id.id,
                    'name'          : partner_id.name,
                    'email'         : partner_id.email,
                    'portal_error'  : f"{e}"
                })
        else:
            counter_already_portal += 1
    self.env.cr.commit()

    _logger.info('************************************************')
    _logger.info('Create and send portal user access concluded')
    _logger.info(f'Emails send: {counter_send}')
    _logger.info(f'Portal User Error: {counter_error}')
    _logger.info(f'Already Portal User: {counter_already_portal}')
    if list_error:
        _logger.info(f'Error User List: {list_error}')
    _logger.info('************************************************')