/** @odoo-module */
import {PosOrder} from "@point_of_sale/app/models/pos_order";
import {patch} from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);
        this.product_temp = loadedData['product.template'];
    }
});



    //     export_for_printing()
    //     {
    //         const result = super.export_for_printing(...arguments);
    //         if (this.get_partner()) {
    //             result.headerData.partner = this.get_partner();
    //         }
    //         return result;
    //     }
    // ,
    // });


// odoo.define('point_of_sale.product_warranty_order_line', function (require) {
//
//     "use strict";
//
//     var {Orderline} = require('point_of_sale.models');
//     const Registries = require('point_of_sale.Registries');
//     const L10nInOrderline = (Orderline) => class L10nInOrderline extends Orderline {
//         export_for_printing() {
//             var line = super.export_for_printing(...arguments);
//             line.product_owner_id = this.get_product().product_owner_id;
//             return line;
//
//         }
//
//     }
//
//     Registries.Model.extend(Orderline, L10nInOrderline);
//
// });
//
