/** @odoo-module */
import {renderToElement} from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

export function _chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

publicWidget.registry.LatestCredit = publicWidget.Widget.extend({
    selector: ".latest_credit_snippet",

    async willStart() {
        const result = await rpc('/get_latest_credit', {});
        console.log("result", result)

        const credits = result;
        console.log("credits",credits)
        Object.assign(this, {credits: credits})
        console.log("this",this)

    },
    start: function () {
        // const refEl = this.$el.find("#top_products_carousel")
        const credits = this.credits;
        const chunks = _chunk(credits, 4)
        console.log("chunks",chunks)
        const random_number = Math.floor(Math.random() * 10);
        console.log(random_number,"random number")
        if (chunks){
        chunks[0].is_active = true;
        }


        this.$(".credit_container").html(renderToElement('recurring_subscription.latest_credit_template', {
            chunks: chunks,
            random: random_number,

        }))


    }
})
