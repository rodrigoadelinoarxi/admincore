/** @odoo-module */

import {Order} from "@point_of_sale/app/store/models";
import {patch} from "@web/core/utils/patch";

patch(Order.prototype, {
    add_orderline(line) {
        super.add_orderline(...arguments);
        let order = this.pos.get_order();
        if (order != null && !order.partner && line.quantity >= 0) {
            if (this.pos.config.end_consumer_partner_id) {
                this.pos._loadPartners([this.pos.config.end_consumer_partner_id[0]]);
                const finalConsumerPartner = this.pos.db.get_partner_by_id(this.pos.config.end_consumer_partner_id[0]);
                if (finalConsumerPartner) {
                    order.set_partner(finalConsumerPartner);
                }
            }
        }
    }
});
