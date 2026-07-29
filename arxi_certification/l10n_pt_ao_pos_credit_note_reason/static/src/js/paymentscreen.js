/** @odoo-module */

import {patch} from "@web/core/utils/patch";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {usePos} from "@point_of_sale/app/store/pos_hook";
import {useService} from "@web/core/utils/hooks";
import { CreditReasonPopup } from "../app/credit_reason_popup/credit_reason_popup";


patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
    },

    async validateOrder(isForceValidate) {
        let order = this.pos.get_order();
        let amount = order.get_total_with_tax()
        if (amount < 0) {
            const {confirmed, payload: result} = await this.popup.add(CreditReasonPopup, {});
            if (!confirmed) {
                return false;
            }
            order.set_credit_reason_text(result.reason_text);
            order.set_refund_type(parseInt(result.refund_type));
            if (result.create_for_future_use) {
                this.orm.call(
                    "account.move.refund.reason",
                    "create_from_ui",
                    [, result.reason_text],
                    {}
                ).then((data) => {
                    this.pos.account_move_refund_reasons.push(data);
                })
            }
        }
        await super.validateOrder(isForceValidate);
    },
});
