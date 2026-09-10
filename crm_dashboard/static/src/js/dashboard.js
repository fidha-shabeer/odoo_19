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


// /** @odoo-module **/
// import {registry} from "@web/core/registry";
// import {Component, useState, useRef, onMounted, onWillStart} from "@odoo/owl";
// import {useService} from "@web/core/utils/hooks";
// import {loadJS} from "@web/core/assets";
// import Chart from 'chart.js/auto';
//
// const actionRegistry = registry.category("actions");
//
// class CrmDashboard extends Component {
//
//     setup() {
//         super.setup();
//         this.orm = this.env.services.orm;
//         this._fetch_data();
//         this.action = useService("action");
//         this.chartRef = useRef("chart");
//
//         // onMounted(() => {
//         //     this.createChart();
//         // });
//
//     }
//
//     // async createChart() {
//     // }
//
//     async _fetch_data() {
//         let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});
//         document.getElementById('my_lead').innerHTML = `<span>${result.total_leads}</span>`;
//         document.getElementById('my_opportunity').innerHTML = `<span>${result.total_opportunity}</span>`;
//         document.getElementById('my_expected_revenue').innerHTML = `<span>${result.currency}${result.expected_revenue}</span>`;
//         document.getElementById('my_revenue').innerHTML = `<span>${result.currency}${result.amount_invoiced}</span>`;
//         document.getElementById('my_ratio').innerHTML = `<span>${result.win_ratio}</span>`;
//     }
//
//     async OpenLead() {
//         console.log("lead card clicked...");
//         let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});
//
//         this.action.doAction({
//             type: "ir.actions.act_window",
//             name: "Lead List",
//             res_model: "crm.lead",
//             view_mode: "list",
//             views: [[false, "list"]],
//             target: "new",
//             domain: [['user_id', '=', result.user_id]],
//         });
//     }
// }
//
// CrmDashboard.template = "crm_dashboard.CrmDashboard";
// // Register the component with the action tag
// actionRegistry.add("crm_dashboard_tag", CrmDashboard);

// /** @odoo-module **/
// // import {registry} from "@web/core/registry";
// import {Component, useState, useRef, onMounted, onWillStart} from "@odoo/owl";
// import {useService} from "@web/core/utils/hooks";
// // import { loadJS } from "@web/core/assets";
// // import Chart from 'chart.js/auto';
//
//
// // const actionRegistry = registry.category("actions");
//
// class CrmDashboard extends Component {
//
//     setup() {
//         super.setup();
//         // onWillStart(async () => {
//         //     await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.1/chart.umd.min.jss");
//         //
//         // })
//         // this.chartRef = useRef("chart")
//         this.orm = this.env.services.orm;
//         this.action = useService("action")
//         this._fetch_data();
//         // this.OpenLead();
//         this.state = useState({
//             won_revenue: 0,
//         })
//
//         // onMounted(() => {
//         //     const data = [
//         //         {year: 2010, count: 10},
//         //         {year: 2011, count: 20},
//         //         {year: 2012, count: 15},
//         //         {year: 2013, count: 25},
//         //         {year: 2014, count: 22},
//         //         {year: 2015, count: 30},
//         //         {year: 2016, count: 28},
//         //     ];
//         //
//         //     new Chart(
//         //         this.chartRef.el,
//         //         {
//         //             type: 'bar',
//         //             data: {
//         //                 labels: data.map(row => row.year),
//         //                 datasets: [
//         //                     {
//         //                         label: 'Acquisitions by year',
//         //                         data: data.map(row => row.count)
//         //                     }
//         //                 ]
//         //             }
//         //         }
//         //     );
//         // });
//
//
//     }
//
//     async _fetch_data() {
//         let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});
//         document.getElementById('my_lead').innerHTML = `<span>${result.total_leads}</span>`;
//         document.getElementById('my_opportunity').innerHTML = `<span>${result.total_opportunity}</span>`;
//         document.getElementById('my_expected_revenue').innerHTML = `<span>${result.currency}${result.expected_revenue}</span>`;
//         document.getElementById('my_revenue').innerHTML = `<span>${result.currency}${result.amount_invoiced}</span>`;
//         document.getElementById('my_ratio').innerHTML = `<span>${result.win_ratio}</span>`;
//     }
//
//     // async OpenLead() {
//     //     console.log("lead card clicked...");
//     //     let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});
//     //
//     //     this.action.doAction({
//     //         type: "ir.actions.act_window",
//     //         name: "Lead List",
//     //         res_model: "crm.lead",
//     //         view_mode: "list",
//     //         views: [[false, "list"]],
//     //         target: "new",
//     //         domain: [['user_id', '==', result.user_id]],
//     //     });
//     // }
//
// }
//
// CrmDashboard.template = "crm_dashboard.CrmDashboard";
// // Register the component with the action tag
// // actionRegistry.add("crm_dashboard_tag", CrmDashboard);