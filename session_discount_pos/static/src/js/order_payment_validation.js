import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import OrderPaymentValidation from "@point_of_sale/app/utils/order_payment_validation";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog, ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        console.log("nfjnvjfn eroroooo")
        const order = this.currentOrder;
        console.log("order",order)
        console.log("ghj",order.globalDiscountPc)
        console.log("session",order.session_id.max_discount_limit)
        if(order.session_id.max_discount_limit<100){
             this.dialog.add(AlertDialog, {
            title: _t("Warning"),
            body: _t("the order discount is greater than global discount!!"),
        });
        }
        return super.validateOrder(isForceValidate)
        }});
        // if (this.pos.config.module_pos_hr) {
        //     this.order.employee_id = this.pos.getCashier();
        // }

