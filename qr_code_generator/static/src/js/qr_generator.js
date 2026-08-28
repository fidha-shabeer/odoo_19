/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, useState} from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";


class QrGenerator extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm')
        // this.state = useState({
            // temp: 0,
            // weather:0,
            // latitude:0,
            // longitude:0,
            // country : null,
            // location:null,
            // time : 0.00,
        // })
    }

    async GenerateQr() {
        console.log("running QR");

    }

}

QrGenerator.template = "qr_icon";
QrGenerator.components = { Dropdown, DropdownItem };
export const systrayItem = {
    Component: QrGenerator,
};
registry.category("systray").add("QrGenerator", systrayItem, {sequence: 1});