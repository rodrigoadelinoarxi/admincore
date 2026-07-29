/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {
    SaleOrderManagementControlPanel
} from '@pos_sale/app/order_management_screen/sale_order_management_control_panel/sale_order_management_control_panel';

const CUSTOM_VALID_SEARCH_TAGS = new Set(["date", "customer", "client", "name", "order", "vat"]);
const CUSTOM_FIELD_MAP = {
    date: "date_order",
    customer: "partner_id.complete_name",
    client: "partner_id.complete_name",
    name: "name",
    order: "name",
    vat: "partner_id.vat",
};
const SEARCH_FIELDS = ["name", "partner_id.complete_name", "date_order", "partner_id.vat"];

patch(SaleOrderManagementControlPanel.prototype, {

    get searchTags() {
        return CUSTOM_VALID_SEARCH_TAGS;
    },

    get fieldMap() {
        return CUSTOM_FIELD_MAP;
    },

    get searchFields() {
        return SEARCH_FIELDS;
    }
});
