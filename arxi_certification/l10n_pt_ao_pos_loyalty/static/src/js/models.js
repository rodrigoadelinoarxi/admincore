/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { OfflineErrorPopup } from "@point_of_sale/app/errors/popups/offline_error_popup";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { _t } from "@web/core/l10n/translation";

    patch(PosStore.prototype, {
        // @Override
        async setup() {
            this.token = "";
            this.vatRateMapping = {};
            await super.setup(...arguments);
        },

    models.load_fields('product.product', 'pos_loyalty_program');

});
