import logging
from odoo import models, fields, api, _, Command
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals_list):
        res = super(SaleOrder, self).create(vals_list)

        self.quant_validation()

        return res

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        self.quant_validation()

        for rec in self:
            rec.confirm_picking_and_send_mail()
        return res

    def quant_validation(self):
        orders_to_conf_picking = []
        for order in self:
            self.verify_categ_quant()
            self.verify_prod_quant()

            if lines_with_categ_limit := order.order_line.filtered(lambda l: l.product_id.categ_id.buy_limit_category):
                bought_quant = sum(lines_with_categ_limit.mapped('product_uom_qty'))
                for line in lines_with_categ_limit:
                    self.env['sale.product.history'].create({
                        'partner_id': order.partner_id.id,
                        'sale_id': order.id,
                        'product_id': line.product_id.id,
                        'product_quant': bought_quant,
                    })

            if order.order_line.filtered(lambda l: l.product_id.categ_id.auto_validate_and_email):
                orders_to_conf_picking.append(order)

    def verify_categ_quant(self):
        problems_list = ''
        lines_with_categ_limit = self.order_line.filtered(lambda l: l.product_id.categ_id.buy_limit_category)
        for categ_id in lines_with_categ_limit.mapped('product_id.categ_id'):
            hist_quant_sum = sum(self.env['sale.product.history'].search(
                [('partner_id', '=', self.partner_id.id), ('product_id.categ_id', '=', categ_id.id)]).mapped(
                'product_quant'))
            sale_quant_sum = sum(
                lines_with_categ_limit.filtered(lambda l: l.product_id.categ_id.id == categ_id.id).mapped(
                    'product_uom_qty'))
            if hist_quant_sum + sale_quant_sum > categ_id.buy_limit_quant:
                problems_list += f'{categ_id.name}, '
        if problems_list:
            self.env.cr.rollback()
            raise ValidationError(_(f'Limit for this Category Products already exceeded [{problems_list}].'))

    def verify_prod_quant(self):
        problems_list = ''
        partner_limited_products = self.partner_id.products_limit_ids.mapped('product_id')
        current_articles = {}
        for limit_product_line in self.order_line.filtered(lambda l: l.product_id in partner_limited_products):

            if limit_product_line.product_id.id in current_articles:
                current_articles[limit_product_line.product_id.id]['counter'] += limit_product_line.product_uom_qty
            else:
                current_articles[limit_product_line.product_id.id] = {'counter' :    limit_product_line.product_uom_qty,
                                                                      'name'    :    limit_product_line.product_id.name}

        for article_id in current_articles:
            if current_articles[article_id]['counter'] > self.env['res.partner.limit'].search(
                    [('product_id', '=', article_id),
                     ('partner_id', '=', self.partner_id.id)], limit=1).quant:
                problems_list += f"{current_articles[article_id]['name']}, "
        if problems_list:
            self.env.cr.rollback()
            raise ValidationError(_(f'Limit for this Products already exceeded [{problems_list}].'))

    def confirm_picking_and_send_mail(self):
        for picking_id in self.picking_ids:
            if lines_to_send := picking_id.move_ids_without_package.filtered(
                    lambda l: l.product_id.categ_id.auto_validate_and_email):
                picking_id.action_assign()
                picking_id.button_validate()
                for categ_id in lines_to_send.mapped('product_id.categ_id'):
                    if categ_id.email_template_id:
                        lang = self.partner_id.lang
                        lot_ids = picking_id.move_ids_without_package.lot_ids.filtered(
                            lambda l: l.product_id.categ_id.id == categ_id.id)
                        attachment_ids = []
                        for lot_id in lot_ids:
                            attachment_ids.append(self.env['ir.attachment'].create({
                                'name': lot_id.file_name,
                                'type': 'binary',
                                'datas': lot_id.file_data,
                                'res_model': 'stock.picking',
                                'res_id': picking_id.id,
                                'mimetype': 'application/pdf',
                            }).id)
                        categ_id.email_template_id.with_context(lang=lang).send_mail(picking_id.id, email_values={
                            'attachment_ids': [Command.set(attachment_ids)]}, force_send=True)
