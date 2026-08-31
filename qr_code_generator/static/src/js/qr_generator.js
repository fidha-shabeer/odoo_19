/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, useState} from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";


class QrGenerator extends Component {
    setup() {
        super.setup();
        this.data;
        this.orm = useService('orm');
        this.action = useService("action");
        this.state = useState({
            qrcode : null,
            text : '',
        })
    }

    async GenerateQr() {
        console.log("hellooo");

        this.action.doAction({
           type: "ir.actions.act_window",
           name: "Generate QR Code",
           res_model: "qr.generate.wizard",
           view_mode: "form",
           views: [[false, "form"]],
           target: "new",
           });


    }

}

QrGenerator.template = "qr_icon";
QrGenerator.components = { Dropdown, DropdownItem };
export const systrayItem = {
    Component: QrGenerator,
};
registry.category("systray").add("QrGenerator", systrayItem, {sequence: 1});