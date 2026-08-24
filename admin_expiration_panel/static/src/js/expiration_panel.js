/** @odoo-module **/

import { ExpirationPanel } from "@web_enterprise/webclient/home_menu/expiration_panel";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";
import { onWillStart } from "@odoo/owl";

patch(ExpirationPanel.prototype, {
    setup() {
        super.setup();
        this.state.displayAlert = true;

        onWillStart(async () => {
            this.state.displayAlert = await user.hasGroup("base.group_erp_manager");
        });
    },
})
