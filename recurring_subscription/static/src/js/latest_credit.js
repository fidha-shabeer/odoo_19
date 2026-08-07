/** @odoo-module */
import {renderToElement} from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

publicWidget.registry.LatestCredit = publicWidget.Widget.extend({
    selector: ".latest_credit_snippet",
    async willStart() {
        const result = await rpc('/get_latest_credit', {});
        console.log("result",result)
        if (result) {
            this.$(".credit_container").html(renderToElement('recurring_subscription.latest_credit_template', {credits: result}))
        }
    },

})