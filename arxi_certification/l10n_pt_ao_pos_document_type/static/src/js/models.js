/** @odoo-module */

import {Order} from "@point_of_sale/app/store/models";
import {patch} from "@web/core/utils/patch";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.document_type = this.document_type || false;
    },

    set_document_type(document_type) {
        this.document_type = document_type;
    },

    get_document_type() {
        return this.document_type;
    },

    isSimplifiedInvoice() {
        return this.document_type === 'FS';
    },

    isNormalInvoice() {
        return this.document_type === 'FT';
    },

    isInvoiceReceipt() {
        return this.document_type === 'FR';
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.document_type = json.document_type || false;
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.document_type = this.document_type || false;
        return json;
    },

});
