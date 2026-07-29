/** @odoo-module */

import {Order} from "@point_of_sale/app/store/models";
import {patch} from "@web/core/utils/patch";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.credit_reason_text = this.credit_reason_text || false;
        this.refund_type = this.refund_type || false;
    },

    set_credit_reason_text(credit_reason_text) {
        this.credit_reason_text = credit_reason_text;
    },

    get_credit_reason_text() {
        return this.credit_reason_text;
    },

    set_refund_type(refund_type) {
        this.refund_type = refund_type;
    },

    get_refund_type() {
        return this.refund_type;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.credit_reason_text = json.credit_reason_text || false;
        this.refund_type = json.refund_type || false;
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.credit_reason_text = this.credit_reason_text || false;
        json.refund_type = this.refund_type || false;
        return json;
    },

    export_for_printing() {
        let result = super.export_for_printing(...arguments);
        result.credit_reason_text = this.credit_reason_text;
        return result;
    },

});
