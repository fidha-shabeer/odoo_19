import {patch} from "@web/core/utils/patch";
import {PosStore} from "@point_of_sale/app/services/pos_store";
import {
    AlertDialog,
    ConfirmationDialog
} from "@web/core/confirmation_dialog/confirmation_dialog";
import {_t} from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async pay() {
        const order = this.getOrder();
        console.log("Order", order)

        const quantity = order.totalQuantity
        console.log("qty", quantity)
        const amount = order.displayPrice;
        console.log("amt", amount)

        const max_limit = order.session_id.max_discount_limit;
        console.log("Max Limit", max_limit)

        const discount = order.getTotalDiscount();
        console.log("disc", discount)

        const total = order.session_id.current_total_discount;
        console.log("current discount total", total);

        let current_total = discount + total;
        console.log("current sum discount", current_total)

        let remaining_discount = max_limit - current_total;
        console.log("remaining", remaining_discount)

        let priceIncl = order.currencyDisplayPriceIncl;
        console.log("price incl", priceIncl)

        let priceExcl = order.currencyDisplayPriceExcl;
        console.log("price excl", priceExcl);

        let globalDisc = order.globalDiscountPc;
        console.log("global disc", globalDisc);

        console.log("this", this)

        console.log("next", order.lines);

        let orderlines = order.lines;
        console.log("orderlines", orderlines);

        if (orderlines) {
            let total = 0;
            orderlines.forEach(line => {
                if (line.productProductPrice) {
                    total += line.productProductPrice;
                    console.log("each", line.productProductPrice);
                }
                ;

            });

            console.log("total amount", total);
            let unitTotal = 0;
            unitTotal = total;
            console.log("unit total price:", unitTotal);

            let globalDisc_price = 0;
            globalDisc_price = unitTotal * globalDisc / 100;
            console.log("global price", globalDisc_price);

            let overall_discount = discount + globalDisc_price + current_total;
            console.log("Overall discount", overall_discount);
            console.log('global',globalDisc_price);
            console.log('current total',current_total);
            console.log('discount line',discount);

            if (remaining_discount && remaining_discount > 0) {
                remaining_discount = max_limit - overall_discount;
            }
            else {
                remaining_discount = 0;
            }
            console.log("remaining discount",remaining_discount)


            if (max_limit && max_limit < overall_discount) {
                this.dialog.add(AlertDialog, {
                    title: _t("Warning"),
                    body: _t("the order discount exceeded the session discount limit, only %s discount left",remaining_discount),
                });
                return;
            }


        }
        ;


        let DiscGlobal = order.globalDiscountPc;
        console.log("global disc", DiscGlobal);


        return super.pay();

    }

})
