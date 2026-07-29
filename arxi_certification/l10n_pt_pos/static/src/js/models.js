/** @odoo-module **/

    import { Order } from "@point_of_sale/app/store/models";
    import { patch } from "@web/core/utils/patch";
    import { _t } from "@web/core/l10n/translation";

    patch(Order.prototype, {
        setup() {
            super.setup(...arguments);
            this.qr_code = this.qr_code || false;
            this.atcud = this.atcud || false;
            this.save_to_db();
        },
        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            if (this.pos.is_pt_country()) {
                this.qr_code = json.qr_code;
                this.atcud = json.atcud;
            }
        },
        set_qr_code(qr_code) {
            this.qr_code = qr_code;
        },
        get_qr_code() {
            return this.qr_code;
        },
        set_atcud(atcud) {
            this.atcud = atcud;
        },
        get_atcud() {
            return this.atcud;
        },
        get_qr_style() {
            return this.pos.config.qr_style;
        },
        export_for_printing() {
            let result = super.export_for_printing(...arguments);
            result.qr_code = this.get_qr_code();
            result.atcud = this.get_atcud();
            result.qr_style = this.get_qr_style();
            return result;
        },
        export_as_JSON() {
            let json = super.export_as_JSON(...arguments);
            json.qr_code = this.get_qr_code();
            json.atcud = this.get_atcud();
            json.qr_style = this.get_qr_style();
            return json;
        },
        _get_qr_code_data() {
            if (this.pos.is_pt_country()) {
                return this.qr_code
            } else {
                return false;
            }
        },
});
