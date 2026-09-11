import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {patch} from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {

    setup() {
        super.setup(...arguments);
        this.orm = this.env.services.orm;
    },

    async validateOrder(isForceValidate) {
        const order = this.currentOrder;
        console.log("Order", order)

        const max_limit = order.session_id.max_discount_limit;
        console.log("Max Limit", max_limit)

        const discount = order.getTotalDiscount();
        console.log("disc", discount)

        const total_disc = order.session_id.current_total_discount;
        console.log("current discount total", total_disc);

        let total = 0;
        let globalDisc_price = 0;
        let unitTotal = 0;
        if (orderlines) {
            orderlines.forEach(line => {
                if (line.productProductPrice) {
                    total += line.productProductPrice;
                }
                ;

            });

            unitTotal = total;
            console.log("unit total price:", unitTotal);

        }
        ;

        let global_price = 0;
        global_price = unitTotal * globalDisc / 100;
        console.log("global price", global_price);


        let overall_discount = globalDisc_price + discount + total_disc;
        console.log("current total discount till now: ", overall_discount);

        globalDisc_price = unitTotal * globalDisc / 100;
        console.log("global price", globalDisc_price);

        let remaining_balance = max_limit - overall_discount;
        console.log("balance", remaining_balance);

        const result = await this.orm.call("pos.session", "max_limit_balance", [order.session_id.id]);
        console.log("result", result)

        let max_balance = 0;
        max_balance = result.max_balance;
        console.log("max balance", max_balance)

        let current = globalDisc_price + discount;
        console.log("current discount",current)

        let balance = 0;
        balance = max_balance - current;
        console.log("current balance",balance)

        await super.validateOrder(isForceValidate);
    },
});
