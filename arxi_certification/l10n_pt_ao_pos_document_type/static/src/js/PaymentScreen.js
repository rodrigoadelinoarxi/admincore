/** @odoo-module **/

import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {patch} from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        const order = this.pos.get_order();
        if (order.get_total_with_tax() > 0) {
            order.set_document_type('FS');
        }
    },

    toggleSimplifiedInvoice() {
        this.currentOrder.set_document_type('FS');
    },

    toggleNormalInvoice() {
        this.currentOrder.set_document_type('FT');
    },

    toggleInvoiceReceipt() {
        this.currentOrder.set_document_type('FR');
    },

});



