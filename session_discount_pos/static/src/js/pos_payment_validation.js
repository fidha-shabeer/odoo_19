import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { AlertDialog, ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async pay(){
        const order = this.getOrder();
        console.log("Order",order)

        const quantity = order.totalQuantity
        console.log("qty",quantity)
        const amount = order.displayPrice;
        console.log("amt",amount)

        const max_limit = order.session_id.max_discount_limit;
        console.log("Max Limit",max_limit)
        const discount = order.getTotalDiscount();
        console.log("disc",discount)

        const total =order.session_id.current_total_discount;
        console.log("current discount total",total);

        let current_total = discount + total;
        console.log("current sum discount",current_total)

        let remaining_discount = max_limit-current_total;
        console.log("remaining",remaining_discount)

        if(remaining_discount<0){
            remaining_discount=0;
        }
        else {
            remaining_discount = max_limit-current_total;
        }

        if(max_limit && current_total>max_limit){
             this.dialog.add(AlertDialog, {
            title: _t("Warning"),
            body: _t("the order discount exceeded the session discount limit,You have %s discount left !!",remaining_discount),
        });
             return;
        }

        return super.pay();

    }

})
