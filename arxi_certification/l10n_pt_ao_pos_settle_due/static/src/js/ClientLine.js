/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";
import { patch } from "@web/core/utils/patch";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { useService } from "@web/core/utils/hooks";

    patch(PartnerListScreen.prototype, {
            async settleCustomerDue() {
                if (this.props.selectedClient == this.props.partner) {
                    ev.stopPropagation();
                }
                const totalDue = this.props.partner.total_due;
                const paymentMethods = this.pos.payment_methods.filter(
                    (method) => this.pos.config.payment_method_ids.includes(method.id) && method.type != 'pay_later'
                );
                const selectionList = paymentMethods.map((paymentMethod) => ({
                    id: paymentMethod.id,
                    label: paymentMethod.name,
                    item: paymentMethod,
                }));
                const {confirmed, payload: selectedPaymentMethod} = await this.popup.add(SelectionPopup, {
                    title: _t('Select the payment method to settle the due'),
                    list: selectionList,
                });
                if (!confirmed) return;
                this.trigger('discard');
                const newOrder = this.pos.add_new_order();
                // Pass specific settle_due parameter to set invoice to false on this specific case
                newOrder.set_to_invoice('settle_due');
                const payment = newOrder.add_paymentline(selectedPaymentMethod);
                payment.set_amount(totalDue);
                newOrder.set_client(this.props.partner);
                this.showScreen('PaymentScreen');
            }
});
