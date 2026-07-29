/** @odoo-module */

import {Order} from "@point_of_sale/app/store/models";
import {patch} from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.invoicing_journal_id = this.invoicing_journal_id || false;
    },

    set_invoicing_journal_id(invoicing_journal_id) {
        this.invoicing_journal_id = invoicing_journal_id;
    },

    isSelectedJournal(journal) {
        return this.invoicing_journal_id === journal.id;
    },

    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.invoicing_journal_id = json.invoicing_journal_id || false;
    },

    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.invoicing_journal_id = this.invoicing_journal_id || false;
        return json;
    },

});

patch(PosStore.prototype, {
    // @Override
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.journals = loadedData['account.journal'];
    },
});
