/** @odoo-module **/

import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {patch} from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.invoicing_journal_map = this.pos.journals.filter(journal => this.pos.config.invoicing_journal_ids.includes(journal.id));
        let order = this.pos.get_order()
        order.set_invoicing_journal_id(this.pos.config.invoice_journal_id[0]);
    },

    toggleJournalInvoice(journal) {
        let order = this.pos.get_order()
        order.set_invoicing_journal_id(journal.id);
    },
});
