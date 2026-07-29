/** @odoo-module */

import {AbstractAwaitablePopup} from "@point_of_sale/app/popup/abstract_awaitable_popup";
import {_t} from "@web/core/l10n/translation";
import {useEffect, useState} from "@odoo/owl";
import {usePos} from "@point_of_sale/app/store/pos_hook";

export class CreditReasonPopup extends AbstractAwaitablePopup {
    static template = "l10n_pt_ao_pos_credit_note_reason.CreditReasonPopup";
    static defaultProps = {
        confirmText: _t("Ok"),
        cancelText: _t("Cancel"),
        title: _t("Credit Reason"),
        body: "",
    };

    /**
     * @param {Object} props
     * @param {string} props.startingValue
     */
    setup() {
        super.setup();
        this.pos = usePos();
        this.values = [...this.pos.account_move_refund_reasons];
        this.values.push({
            'id': 'other',
            'name': _t('Other'),
        })
        this.refundTypes = [...this.pos.refund_type];
        this.refundTypeLabel = _t("Refund Type");
        this.state = useState({
            credit_reasons: this.values[0].id,
            refund_type: this.refundTypes[0]?.id || null,
            custom_value: "",
            is_custom: false,
            create_for_future_use: false
        });
        useEffect(
            () => {
                this.state.is_custom = this.state.create_for_future_use = this.state.credit_reasons === 'other';
            },
            () => [this.state.credit_reasons],
        );
    }

    async confirm() {
        let reason_text;
        if (this.state.is_custom) {
            if (!this.state.custom_value) {
                // If custom value is empty, show a message and return
                alert(_t("Custom value is required"));
                return;
            }
            reason_text = this.state.custom_value;
        } else {
            // Find the reason text from the values array
            const selectedReason = this.values.find(reason => String(reason.id) === String(this.state.credit_reasons));
            reason_text = selectedReason ? selectedReason.name : "";
        }

        this.props.close({
            confirmed: true,
            payload: {
                reason_text: reason_text,
                refund_type: this.state.refund_type,
                create_for_future_use: this.state.create_for_future_use,
            },
        });
    }

    onReasonChange(event) {
        this.state.credit_reasons = event.target.value;
    }

    onRefundTypeChange(event) {
        this.state.refund_type = event.target.value;
    }

    cancel() {
        this.props.close({confirmed: false});
    }

}
