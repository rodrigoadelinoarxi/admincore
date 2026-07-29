/** @odoo-module */

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";

patch(ReceiptScreen.prototype, {
        setup() {
            super.setup(...arguments);
        },

        // Standard print: from the 2nd print onward, mark doc_printed before printing
        async printReceipt() {
            try {
                const order = this.currentOrder;
                if (order && order._printed && !order.doc_printed) {
                    order.doc_printed = true;
                }
            } catch (_) {}

            await super.printReceipt(...arguments);

            // Persist doc_printed if already flagged and order exists server-side
            try {
                const order = this.currentOrder;
                if (order?.doc_printed && typeof order.server_id === "number") {
                    await this.pos.orm.write("pos.order", [order.server_id], { doc_printed: true });
                }
            } catch (_) {}
        },

        async printDuplicateReceipt() {
            const isPrinted = await this.printer.print(
                OrderReceipt,
                {
                    data: {
                        ...this.pos.get_order().export_for_printing(),
                        is_duplicated_print: true,
                    },
                    formatCurrency: this.env.utils.formatCurrency,
                },
                { webPrintFallback: true }
            );

            if (isPrinted) {
                this.currentOrder._printed = true;
            }

            if (this.buttonPrintReceipt.el) {
                this.buttonPrintReceipt.el.className = "fa fa-print";
            }
        },

        async printTriplicateReceipt() {
            const isPrinted = await this.printer.print(
                OrderReceipt,
                {
                    data: {
                        ...this.pos.get_order().export_for_printing(),
                        is_triplicate_print: true,
                    },
                    formatCurrency: this.env.utils.formatCurrency,
                },
                { webPrintFallback: true }
            );

            if (isPrinted) {
                this.currentOrder._printed = true;
            }

            if (this.buttonPrintReceipt.el) {
                this.buttonPrintReceipt.el.className = "fa fa-print";
            }
        },
});
