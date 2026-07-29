/** @odoo-module */

import {registry} from "@web/core/registry";
import {downloadReport} from "@web/webclient/actions/reports/utils";

// Get the existing reportService
const reportService = registry.category("services").get("report");

// Extend the reportService
reportService.start = (function (original) {
    const reportActionsCache = {};
    return async function (env, {rpc, user, ui, orm, pos}) {
        const originalService = await original.apply(this, arguments);

        // Extend the original doAction method
        const originalDoAction = originalService.doAction;
        originalService.doAction = async function (reportXmlId, active_ids) {
            ui.block();
            try {
                if (reportXmlId === "account.account_invoices") {
                    // CUSTOM -> Ignore downloading this report as it is not certified
                    return false;
                } else {
                    // Default behavior
                    const reportAction = reportActionsCache[reportXmlId] || await rpc("/web/action/load", {
                        action_id: reportXmlId,
                    });
                    reportActionsCache[reportXmlId] = reportAction;
                    await downloadReport(
                        rpc,
                        {...reportAction, context: {active_ids}},
                        "pdf",
                        user.context
                    );
                }
            } finally {
                ui.unblock();
            }
        };

        return originalService;
    };
})(reportService.start);
