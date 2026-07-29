/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {ErrorPopup} from "@point_of_sale/app/errors/popups/error_popup";
import {patch} from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async _postPushOrderResolve(order, order_server_ids) {
        if (this.pos.is_pt_ao_country()) {
            const result = await this.orm.searchRead(
                'pos.order',
                [['id', 'in', order_server_ids]],
                ['inalterable_hash', 'account_move_name', 'document_name', 'credit_reason', 'reversed_entry_name', 'account_move_state', 'cashier_name', 'customer_name', 'customer_vat', 'exemption_codes'],
            );
            order.set_inalterable_hash(result[0].inalterable_hash || false);
            order.set_account_move_name(result[0].account_move_name || false);
            order.set_account_move_state(result[0].account_move_state || false);
            order.set_document_name(result[0].document_name || false);
            order.set_credit_reason(result[0].credit_reason || false);
            order.set_reversed_entry_name(result[0].reversed_entry_name || false);
            order.set_cashier_name(result[0].cashier_name || this.pos.get_cashier().name);
            order.set_customer_name(result[0].customer_name || order.get_partner()?.name || '');
            order.set_customer_vat(result[0].customer_vat || order.get_partner()?.vat || '');
            order.set_exemption_codes(result[0].exemption_codes || false);
        }
        return super._postPushOrderResolve(...arguments);
    },

    //@override
    async _isOrderValid(isForceValidate) {
        let res = await super._isOrderValid(...arguments);
        self = this
        if (this.pos.get_order().get_partner()) {
            await this.pos.get_order().get_orderlines().forEach(function (line) {
                if (!line.product.taxes_id.length) {
                    self.popup.add(ErrorPopup, {
                        title: _t('Error in Taxes on Lines'),
                        body: _t('There are lines without taxes.'),
                    });
                    res = false;
                }
            });
        }
        return res;
    },
});



