/** @odoo-module **/

    import { PosStore } from "@point_of_sale/app/store/pos_store";
    import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
    import { patch } from "@web/core/utils/patch";

    patch(PosStore.prototype, {
        is_pt_ao_country() {
            let countries = ['PT', 'AO'];
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


