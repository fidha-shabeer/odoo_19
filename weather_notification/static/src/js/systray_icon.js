/** @odoo-module **/
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component, useState} from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";


class SystrayIcon extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm')
        this.state = useState({
            temp: 0,
            weather:0,
            latitude:0,
            longitude:0,
            country : null,
            location:null,
            time : 0.00,
        })
        this.notification = useService("notification");


    }

    async showNotification() {
        console.log("peijjnfjr")
        let result = await this.orm.call("weather.notification", "get_weather", []);
        console.log("result", result);
        this.state.weather = result.weather;
        console.log("weather",this.state.weather);
        this.state.temp = result.temp;
        console.log("temp",this.state.temp);
        this.state.location= result.data.name;
        console.log("city",this.state.location)
        this.state.country = result.data.sys.country;
        console.log("country",this.state.country)
        this.state.time = result.time;
        console.log("time",this.state.time)





        // this.notification.add(` \n Temperature:  ${this.state.temp}`, {
        //     title: "Weather Notification \n ",
        //     type: "info",
        //     sticky: false,
        // });
    }


}

SystrayIcon.template = "systray_icon";
SystrayIcon.components = { Dropdown, DropdownItem };
export const systrayItem = {
    Component: SystrayIcon,
};
registry.category("systray").add("SystrayIcon", systrayItem, {sequence: 1});