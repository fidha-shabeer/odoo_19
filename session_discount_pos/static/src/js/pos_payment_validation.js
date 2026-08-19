import {patch} from "@web/core/utils/patch";
import {PosStore} from "@point_of_sale/app/services/pos_store";
import {
    AlertDialog,
    ConfirmationDialog
} from "@web/core/confirmation_dialog/confirmation_dialog";
import {_t} from "@web/core/l10n/translation";


patch(PosStore.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = this.env.services.orm;
    },
    async pay() {


        const order = this.getOrder();
        console.log("Order", order)

        const max_limit = order.session_id.max_discount_limit;
        console.log("Max Limit", max_limit)

        const discount = order.getTotalDiscount();
        console.log("disc", discount)
        order.set_discount_amount(discount);

        const total_disc = order.session_id.current_total_discount;
        console.log("current discount total", total_disc);

        let globalDisc = order.globalDiscountPc;
        console.log("global disc", globalDisc);

        let orderlines = order.lines;
        console.log("orderlines", orderlines);

        let total = 0;
        let unitTotal = 0;
        if (orderlines) {
            orderlines.forEach(line => {
                if (line.productProductPrice) {
                    total += line.productProductPrice;
                    console.log("each", line.productProductPrice);
                }
                ;

            });

            unitTotal = total;
            console.log("unit total price:", unitTotal);

        }
        ;

        let globalDisc_price = 0;
        globalDisc_price = unitTotal * globalDisc / 100;
        console.log("global price", globalDisc_price);

        order.set_global_discount_amount(globalDisc_price);

        let current_total = globalDisc_price + discount + total_disc;
        console.log("current total discount till now: ", current_total);

        let current_discount = globalDisc_price + discount
        current_discount = globalDisc_price + discount
        console.log("current discount",current_total)


        const result = await this.orm.call("pos.session", "max_limit_balance", [order.session_id.id]);
        console.log("result", result)

        let max_balance = 0;
        max_balance = result.max_balance;
        console.log("max balance", max_balance)


        if (current_discount > max_balance) {
            this.dialog.add(AlertDialog, {
                title: _t("Warning"),
                body: _t("the order discount exceeded the session discount limit, only %s discount left", max_balance),
            });
            return;
        }


        return super.pay();
    },

})

