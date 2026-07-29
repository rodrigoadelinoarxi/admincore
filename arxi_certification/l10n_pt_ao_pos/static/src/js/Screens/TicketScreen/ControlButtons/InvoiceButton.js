/** @odoo-module */

    import { InvoiceButton } from "@point_of_sale/app/screens/ticket_screen/invoice_button/invoice_button";
    import { patch } from "@web/core/utils/patch";

    patch(InvoiceButton.prototype, {
    async _downloadInvoice(orderId) {
        try {
            const [orderWithInvoice] = await this.orm.read(
                "pos.order",
                [orderId],
                ["account_move", "inalterable_hash"],
                { load: false }
            );
            if (orderWithInvoice?.account_move) {
                if (orderWithInvoice.inalterable_hash) {
                    await this.report.doAction("account.account_invoices_without_payment", [
                        orderWithInvoice.account_move
                    ]);
                } else {
                    await this.report.doAction("account.account_invoices", [
                        orderWithInvoice.account_move
                    ]);
                }
            }
        } catch (error) {
            if (error instanceof Error) {
                throw error;
            } else {
                // NOTE: error here is most probably undefined
                this.popup.add(ErrorPopup, {
                    title: _t("Network Error"),
                    body: _t("Unable to download invoice."),
                });
            }
        }
    }
});