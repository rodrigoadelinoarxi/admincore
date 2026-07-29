/** @odoo-module **/

import { ExpirationPanel } from "@web_enterprise/webclient/home_menu/expiration_panel";
import { patch } from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";

patch(ExpirationPanel.prototype, {
    setup() {
        super.setup();
        this.user = useService("user");
        this.state.displayAlert = true;

        onWillStart(async () => {
            this.state.displayAlert = await this.user.hasGroup("base.group_erp_manager");
        });
    },
})

