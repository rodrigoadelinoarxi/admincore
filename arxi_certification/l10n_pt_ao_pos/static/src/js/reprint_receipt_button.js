/** @odoo-module */

import {ReprintReceiptScreen} from "@point_of_sale/app/screens/receipt_screen/reprint_receipt_screen";
import {patch} from "@web/core/utils/patch";
import {OrderReceipt} from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";

patch(ReprintReceiptScreen.prototype, {
    async tryReprint() {
        let data = this.props.order.export_for_printing();
        data['reprint'] = true;
        // For explicit reprint, force copy labeling pre-print
        data['doc_printed'] = true;

        await this.printer.print(
            OrderReceipt,
            {
                data: data,
                formatCurrency: this.env.utils.formatCurrency,
            },
            {webPrintFallback: true}
        );
        // Persist doc_printed after reprint
        try {
            const order = this.props.order;
            if (order && !order.doc_printed) {
                order.doc_printed = true;
                if (typeof order.server_id === 'number') {
                    await this.pos.orm.write('pos.order', [order.server_id], { doc_printed: true });
                }
            }
        } catch (_) {}
    },

    async printDuplicateReceipt() {
        let data = this.props.order.export_for_printing();
        data['is_duplicated_print'] = true;

        await this.printer.print(
            OrderReceipt,
            {
                data: data,
                formatCurrency: this.env.utils.formatCurrency,
            },
            {webPrintFallback: true}
        );
        // After manual duplicate reprint, mark and persist doc_printed
        try {
            const order = this.props.order;
            if (order && !order.doc_printed) {
                order.doc_printed = true;
                if (typeof order.server_id === 'number') {
                    await this.pos.orm.write('pos.order', [order.server_id], { doc_printed: true });
                }
            }
        } catch (_) {}
    },

    async printTriplicateReceipt() {
        let data = this.props.order.export_for_printing();
        data['is_triplicate_print'] = true;

        await this.printer.print(
            OrderReceipt,
            {
                data: data,
                formatCurrency: this.env.utils.formatCurrency,
            },
            {webPrintFallback: true}
        );
        // After manual triplicate reprint, mark and persist doc_printed
        try {
            const order = this.props.order;
            if (order && !order.doc_printed) {
                order.doc_printed = true;
                if (typeof order.server_id === 'number') {
                    await this.pos.orm.write('pos.order', [order.server_id], { doc_printed: true });
                }
            }
        } catch (_) {}
    }
});
