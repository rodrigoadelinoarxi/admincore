/** @odoo-module **/

    import { PosStore } from "@point_of_sale/app/store/pos_store";
    import { patch } from "@web/core/utils/patch";
    import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

    patch(PosStore.prototype, {
        is_pt_country() {
            let countries = ['PT'];
            if (!this.company.country) {
                self.popup.add(ErrorPopup, {
                    'title': _t("Missing Country"),
                    'body': _.str.sprintf(_t('The company %s doesn\'t have a country set.'), this.company.name),
                });
                return false;
            }
            if (countries.includes(this.company.country.code)) {
                return true;
            }
            else{
                return false;
            }
        },
});
