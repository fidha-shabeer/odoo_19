/** @odoo-module **/
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
patch(PosOrder.prototype, {
   setup(vals) {
       super.setup(vals);
       this.global_discount_amount =
           vals.global_discount_amount || "";

       this.discount_amount = vals.discount_amount || "";
       },

    set_global_discount_amount(globalDisc_price) {
       this.global_discount_amount = globalDisc_price;},
    set_discount_amount(discount){
       this.discount_amount = discount;
    }



});