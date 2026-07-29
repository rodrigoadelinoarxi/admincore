/** @odoo-module **/

import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {patch} from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async _postPushOrderResolve(order, order_server_ids) {
        if (this.pos.is_pt_country()) {
            const result = await this.orm.searchRead(
                'pos.order',
                [['id', 'in', order_server_ids]],
                ['inalterable_hash', 'atcud', 'qr_code', 'account_move_name', 'document_name'],
            );
            order.set_qr_code(result[0].qr_code || false);
            order.set_atcud(result[0].atcud || false);
        }
        return super._postPushOrderResolve(...arguments);
    }
});
