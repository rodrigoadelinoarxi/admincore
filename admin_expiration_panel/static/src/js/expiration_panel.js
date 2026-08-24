/** @odoo-module **/

import { ExpirationPanel } from "@web_enterprise/webclient/home_menu/expiration_panel";
import { patch } from "@web/core/utils/patch";
import { user } from "@web/core/user";
import { onWillStart } from "@odoo/owl";

patch(ExpirationPanel.prototype, {
    setup() {
        super.setup();
        // useService("user")/this.env.services.user rebentavam o arranque do
        // HomeMenu inteiro no Odoo 19 ("Service user is not available" /
        // "Cannot read properties of undefined") — o ExpirationPanel é
        // montado num contexto de Owl onde o serviço "user" ainda não está
        // disponível. O módulo singleton "@web/core/user" expõe a mesma
        // informação (incl. hasGroup) sem depender do sistema de serviços.
        this.user = user;
        this.state.displayAlert = true;

        onWillStart(async () => {
            this.state.displayAlert = await this.user.hasGroup("base.group_erp_manager");
        });
    },
})

