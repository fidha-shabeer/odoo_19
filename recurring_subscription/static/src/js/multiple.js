/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.subscriptionForm = publicWidget.Widget.extend({
    selector: '.subscription-form',

    events: {
        "submit": "_onSubmit",
    },
    start() {
        console.log("loading...");
        return this._super();
    },

    _onSubmit(ev) {
        console.log("gdegduegfu")
        const establishment = this.$('#establishment_id').val()
        const amount = this.$('#amount_id').val()

        // const est_val = establishment.values
        // const amount_val = amount.values

        console.log(amount)
        console.log(establishment)

        // let pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{8,}$/;
        //
        // if (!pattern.test(establishment)) {
        //     console.log("6789");
        //     // alert("not valid");
        //     $('#est_error').text("Password must be at least 8 characters");
        //     // document.getElementById("est_error").innerHTML = "Password must be at least 8 characters";
        //     ev.preventDefault();
        // }

        if (amount < 1) {
            console.log("heuhr workingg");
            $('#amt_error').text("Amount should be >0");
            // alert("must be greater than 0");
            ev.preventDefault();
            return;
        }


        // //
        // console.log("jiurhb");


        // else {
        //     document.getElementById("est_error").innerHTML = "Id should contain 3 letter 3 digits and 2 spcl char";
        //     ev.preventDefault();
        // }

    }

})



