/** @odoo-module **/

import { Order, Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.to_invoice = true;
        this.inalterable_hash = this.inalterable_hash || false;
        this.account_move_name = this.account_move_name || false;
        this.document_name = this.document_name || false;
        this.credit_reason = this.credit_reason || false;
        this.reversed_entry_name = this.reversed_entry_name || false;
        this.account_move_state = this.account_move_state || false;
        this.cashier_name = this.cashier_name || false;
        this.customer_name = this.customer_name || false;
        this.customer_vat = this.customer_vat || false;
        this.exemption_codes = this.exemption_codes || false;
        this.doc_printed = this.doc_printed || false;
        this.save_to_db();
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        if (this.pos.is_pt_ao_country()) {
            this.inalterable_hash = json.inalterable_hash;
            this.account_move_name = json.account_move_name;
            this.document_name = json.document_name;
            this.credit_reason = json.credit_reason;
            this.reversed_entry_name = json.reversed_entry_name;
            this.account_move_state = json.account_move_state;
            this.cashier_name = json.cashier_name;
            this.customer_name = json.customer_name;
            this.customer_vat = json.customer_vat;
            this.exemption_codes = json.exemption_codes;
            this.doc_printed = json.doc_printed || false;
        }
    },
    set_cashier_name(cashier_name) {
        this.cashier_name = cashier_name;
    },
    get_cashier_name() {
        return this.cashier_name;
    },
    set_customer_name(customer_name) {
        this.customer_name = customer_name;
    },
    get_customer_name() {
        return this.customer_name;
    },
    set_customer_vat(customer_vat) {
        this.customer_vat = customer_vat;
    },
    get_customer_vat() {
        if (this.pos.company.country.code === 'PT' && (this.customer_vat === '999999990' || !this.customer_vat)) {
            return '---------'
        }
        if (this.pos.company.country.code === 'AO' && (this.customer_vat === '999999999' || !this.customer_vat)) {
            return '---------'
        }
        return this.customer_vat;
    },
    set_to_invoice(to_invoice) {
        this.assert_editable();
        this.to_invoice = true;
    },
    set_inalterable_hash(inalterable_hash) {
        this.inalterable_hash = inalterable_hash;
    },
    get_inalterable_hash() {
        return this.inalterable_hash;
    },
    set_reversed_entry_name(reversed_entry_name) {
        this.reversed_entry_name = reversed_entry_name;
    },
    get_reversed_entry_name() {
        return this.reversed_entry_name;
    },
    set_account_move_state(account_move_state) {
        this.account_move_state = account_move_state;
    },
    get_account_move_state() {
        return this.account_move_state;
    },
    set_credit_reason(credit_reason) {
        this.credit_reason = credit_reason;
    },
    get_credit_reason() {
        return this.credit_reason;
    },
    set_account_move_name(account_move_name) {
        this.account_move_name = account_move_name;
    },
    get_account_move_name() {
        return this.account_move_name;
    },
    set_document_name(document_name) {
        this.document_name = document_name;
    },
    get_document_name() {
        return this.document_name;
    },
    set_exemption_codes(exemption_codes) {
        this.exemption_codes = exemption_codes;
    },
    wait_for_push_order() {
        var result = super.wait_for_push_order(...arguments);
        result = Boolean(result || this.pos.is_pt_ao_country());
        return result;
    },
    destroy(option) {
        if (option && option.reason == 'abandon' && this.pos.is_pt_ao_country() && this.get_orderlines().length) {
            self.popup.add(ErrorPopup, {
                'title': _t("Fiscal Data Module error"),
                'body': _t("Deleting of orders is not allowed."),
            });
            return false;
        } else {
            super.destroy(...arguments);
        }
    },
    export_for_printing() {
        let result = super.export_for_printing(...arguments);
        result.inalterable_hash = this.get_inalterable_hash();
        result.account_move_name = this.get_account_move_name();
        result.customer_vat = this.get_customer_vat();
        result.customer_name = this.get_customer_name();
        result.document_name = this.get_document_name();
        result.credit_reason = this.get_credit_reason();
        result.reversed_entry_name = this.get_reversed_entry_name();
        result.account_move_state = this.get_account_move_state();
        result.cashier_name = this.get_cashier_name();
        result.partner = this.partner;
        result.doc_printed = this.doc_printed || false;

        // Parse exemption codes here in JavaScript, not in template
        if (this.exemption_codes) {
            try {
                if (typeof this.exemption_codes === 'string') {
                    result.exemption_codes = JSON.parse(this.exemption_codes);
                } else {
                    result.exemption_codes = this.exemption_codes;
                }
            } catch (error) {
                console.error('Error parsing exemption codes:', error);
                result.exemption_codes = {};
            }
        }

        return result;
    },

    export_as_JSON() {
        let json = super.export_as_JSON(...arguments);
        json.inalterable_hash = this.inalterable_hash;
        json.account_move_name = this.account_move_name;
        json.credit_reason = this.credit_reason;
        json.reversed_entry_name = this.reversed_entry_name;
        json.document_name = this.document_name;
        json.account_move_state = this.account_move_state;
        json.cashier_name = this.cashier_name;
        json.customer_name = this.customer_name;
        json.customer_vat = this.customer_vat;
        json.exemption_codes = this.exemption_codes;
        json.doc_printed = this.doc_printed || false;
        return json;
    },
});

patch(Orderline.prototype, {
    getDisplayData() {
        let display_tax = 0;
        if (this.tax_ids) {
            display_tax = this.tax_ids.length > 0 ? this.pos.taxes_by_id[this.tax_ids[0]].invoice_label : 0
        } else {
            display_tax = this.product.taxes_id.length > 0 ? this.pos.taxes_by_id[this.product.taxes_id[0]].invoice_label : 0
        }
        return {
            ...super.getDisplayData(),
            tax: display_tax,
        };
    },
});
