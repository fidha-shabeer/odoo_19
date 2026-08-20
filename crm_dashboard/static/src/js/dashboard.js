/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component} from "@odoo/owl";

const actionRegistry = registry.category("actions");

class CrmDashboard extends Component {

    setup() {
        super.setup();
        this.orm = this.env.services.orm;
        this._fetch_data();
    }

    async _fetch_data() {
        let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});
        document.getElementById('my_lead').innerHTML = `<span>${result.total_leads}</span>`;
        document.getElementById('my_opportunity').innerHTML = `<span>${result.total_opportunity}</span>`;
        document.getElementById('my_expected_revenue').innerHTML = `<span>${result.currency}${result.expected_revenue}</span>`;
    }
}

CrmDashboard.template = "crm_dashboard.CrmDashboard";
// Register the component with the action tag
actionRegistry.add("crm_dashboard_tag", CrmDashboard);