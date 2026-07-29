odoo.define('l10n_pt_ao_pos_loyalty.loyalty', function (require) {
    'use strict';

    var models = require('point_of_sale.models');
    var utils = require('web.utils');
    var core = require('web.core');
    var _t = core._t;
    import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
    var round_pr = utils.round_precision;
    var OrderlineSuper = models.Orderline.prototype;
    var OrderSuper = models.Order.prototype;
    models.load_fields('res.partner', 'loyalty_program');

    models.Order = models.Order.extend({
        apply_reward: function (reward) {
            // Validate lines if has reward and return error
            for (var line of this.get_orderlines()) {
                if (line.reward_id) {
                    self.popup.add(ErrorPopup, {
                        'title': _t('Pos Error'),
                        'body': _t('You cannot apply two rewards at the same time'),
                    });
                    return;
                }
            }

            var client = this.get_client();
            if (!client.loyalty_program) {
                self.popup.add(ErrorPopup, {
                    'title': _t('Pos Error'),
                    'body': _t('The selected customer has Loyalty program disabled.'),
                });
                return;
            }
            var product, product_price, order_total, spendable, line_discount;
            var crounding;

            if (!client) {
                return;
            } else if (reward.reward_type === 'gift') {
                product = this.pos.db.get_product_by_id(reward.gift_product_id[0]);

                if (!product) {
                    return;
                }

                this.add_product(product, {
                    price: 0,
                    quantity: 1,
                    merge: false,
                    extras: {reward_id: reward.id},
                });

            } else if (reward.reward_type === 'discount') {
                crounding = this.pos.currency.rounding;
                spendable = this.get_spendable_points();
                order_total = this.get_total_without_tax();
                var discount = 0;

                product = this.pos.db.get_product_by_id(reward.discount_product_id[0]);

                if (!product) {
                    return;
                }

                if (reward.discount_type === "percentage") {
                    if (reward.discount_apply_on === "on_order") {
                        discount += round_pr(order_total * (reward.discount_percentage / 100), crounding);
                        for (var line of this.get_orderlines()) {
                            if (line.discount)
                                line_discount = reward.discount_percentage + line.discount;
                            else
                                line_discount = reward.discount_percentage;
                            line.set_discount(line_discount);
                        }
                    }

                    if (reward.discount_apply_on === "specific_products") {
                        for (var prod of reward.discount_specific_product_ids) {
                            var specific_products = this.pos.db.get_product_by_id(prod);

                            if (!specific_products)
                                return;

                            for (let line of this.get_orderlines()) {
                                if (line.product.id === specific_products.id) {
                                    discount += round_pr(line.get_price_without_tax() * (reward.discount_percentage / 100), crounding);
                                    if (line.discount)
                                        line_discount = reward.discount_percentage + line.discount;
                                    else
                                        line_discount = reward.discount_percentage;
                                    line.set_discount(line_discount);
                                }
                            }
                        }
                    }

                    if (reward.discount_apply_on === "cheapest_product") {
                        let lines = this.get_orderlines();
                        let lowest_price_line = null;
                        for (let line of lines) {
                            if (lowest_price_line === null || line.price < lowest_price_line.price) {
                                lowest_price_line = line
                            }
                        }
                        discount = round_pr(lowest_price_line.get_price_without_tax() * (reward.discount_percentage / 100), crounding);
                        if (lowest_price_line.discount)
                            line_discount = reward.discount_percentage + lowest_price_line.discount;
                        else
                            line_discount = reward.discount_percentage;
                        lowest_price_line.set_discount(line_discount);
                    }

                    if (reward.discount_max_amount !== 0 && discount > reward.discount_max_amount) {
                        let new_discount = 100.0 - (((order_total - reward.discount_max_amount) * 100) / order_total)
                        for (let line of this.get_orderlines()) {
                            if (line.discount)
                                line_discount = new_discount + line.discount;
                            else
                                line_discount = new_discount;
                            line.set_discount(line_discount);
                        }
                    }
                }
                // We need to add this product to remove the loyalty points, and the reward matches with the quantity
                // if we added the reward to an existing line, we would have quantity_line * reward cost and it would
                // not match
                this.add_product(product, {
                    price: (reward.discount_type === "percentage") ? 0 : -reward.discount_fixed_amount,
                    quantity: 1,
                    merge: false,
                    extras: {reward_id: reward.id},
                });
            }
        },
        remove_orderline: function (line) {
            // If removing reward product lines we must clear all lines so we don't add multiple rewards at the same time
            OrderSuper.remove_orderline.apply(this, arguments);
            if (line.reward_id) {
                for (var order_line of this.get_orderlines()) {
                    this.remove_orderline(order_line);
                }
            }
        },
        add_product: function (product, options) {
            // As we can't remove the pos_loaylaty_program products we validate it before adding products
            if (product.pos_loyalty_program && !options.extras)
                self.popup.add(ErrorPopup, {
                    'title': _t('Pos Error'),
                    'body': _t('You cannot add Loyalty program products'),
                });
            else {
                OrderSuper.add_product.apply(this, arguments);
            }
        },
    });

    models.Orderline = models.Orderline.extend({
        set_discount: function (discount) {
            OrderlineSuper.set_discount.apply(this, arguments);
            // 2 Decimal places for the POS UI
            this.discountStr = '' + this.discount.toFixed(2);
        },
    });
})
