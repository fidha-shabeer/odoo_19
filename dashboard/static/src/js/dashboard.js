/** @odoo-module **/
import {registry} from "@web/core/registry";
import {Component, useState, useRef, onMounted, onWillStart} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";
import {loadJS} from "@web/core/assets";


const actionRegistry = registry.category("actions");

class CrmDashboard extends Component {

    setup() {
      super.setup();
        this.state = useState({
            monthLead: {},
            period: "year",
            is_manager:false,
        });

        onWillStart(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.5.1/chart.umd.min.js");

        })
        onMounted(() => {
            this.createChart();
            this.activityChart();
            this.doughnut();
            this.campaign();
            this.monthLead();

        });

        this.chartRef = useRef("chart");
        this.ActivityChart = useRef("activityChart");
        this.doughnutChartRef = useRef('doughnut');
        this.lineChart = useRef('line');
        this.myChart = null;
        this.myChartdough = null;
        this.myChartbar = null;
        this.myChartpie = null;
        this.orm = this.env.services.orm;
        this._fetch_data();
        this.action = useService("action");
    }

    async _fetch_data() {
        let result = await this.orm.call("crm.lead", "get_tiles_data", [this.state.period], {});
        document.getElementById('my_lead').innerHTML = `<span>${result.total_leads}</span>`;
        document.getElementById('my_opportunity').innerHTML = `<span>${result.total_opportunity}</span>`;
        document.getElementById('my_expected_revenue').innerHTML = `<span>${result.currency}${result.expected_revenue}</span>`;
        document.getElementById('my_revenue').innerHTML = `<span>${result.currency}${result.amount_invoiced}</span>`;
        document.getElementById('my_ratio').innerHTML = `<span>${result.win_ratio}</span>`;
    }

    async onChangePeriod(ev) {
        console.log("filter changer!", ev);
        console.log("ev value", ev.target.value);
        this.state.period = ev.target.value;
        console.log("final value", this.state.period);
        await this._fetch_data();
        await this.campaign();
        await this.doughnut();
        await this.createChart();
        await this.activityChart();


    }


    async createChart() {
        let result = await this.orm.call("crm.lead", "get_lost_data", [this.state.period], {});
        console.log("fghj", result);
        if(this.myChartbar){
            this.myChartbar.destroy();
        }

        this.myChartbar = new Chart(this.chartRef.el, {
            type: 'bar',
            data: {
                labels: result.map(row => row.label),
                datasets: [
                    {
                        label: 'LOST OPPORTUNITY',
                        data: result.map(row => row.count)
                    }
                ]
            }
        });

    };

    async doughnut() {
        let result = await this.orm.call("crm.lead", "get_medium_data", [this.state.period], {});
        console.log("printtt", result);

        if(this.myChartdough){
         this.myChartdough.destroy();
}
        this.myChartdough = new Chart(this.doughnutChartRef.el, {
            type: "doughnut",
            data: {
                labels: result.map(row => row.medium),
                datasets: [{
                    backgroundColor: ["#2d689a", "#8f4f4a", "#1f4924", "#855832", "#7FDBFF", "#B10DC9", "#FFDC00", "#001f3f", "#39CCCC", "#01FF70", "#85144b", "#F012BE", "#3D9970", "#111111", "#AAAAAA"],
                    data: result.map(row => row.count),
                    hoverOffset: 4,
                }]
            },
            options: {}
        });

    }

    async monthLead() {
        let result = await this.orm.call("crm.lead", "get_lead_month_data", [], {});
        console.log("result month", result);

        this.state.monthLead = result;
        console.log("hjk", this.state.monthLead)
    }


    async activityChart() {
        let result = await this.orm.call("crm.lead", "get_activity_data", [this.state.period], {});
        console.log("res", result);
        if(this.myChartpie){
            this.myChartpie.destroy();
        }
        this.myChartpie= new Chart(this.ActivityChart.el, {
            type: "pie",
            data: {
                labels: result.map(row => row.label),
                datasets: [{
                    backgroundColor: ["#874263", "#471a3c", "#69ac8e", "#111111", "#AAAAAA"],
                    data: result.map(row => row.count),
                    hoverOffset: 4,
                }]
            },
            options: {}
        });
    }

    async campaign() {
        let result = await this.orm.call("crm.lead", "get_campaign_data", [this.state.period], {});
        console.log("campaign", result);

        if(this.myChart){
       this.myChart.destroy();
}
        this.myChart = new Chart(this.lineChart.el, {
            type: "line",
            data: {
                labels: result.map(row => row.campaign),
                datasets: [{
                    label: "campaigns",
                    backgroundColor: "blue",
                    data: result.map(row => row.count),
                    hoverOffset: 4,
                }]
            },
            options: {}
        });


    }

    async OpenLead() {
        console.log("lead card clicked...");
        let result = await this.orm.call("crm.lead", "get_tiles_data", [this.state.period], {});
        this.state.is_manager=result.manager_grp;
        console.log("is manager",this.state.is_manager)

        if (this.state.is_manager){
            this.action.doAction({
            type: "ir.actions.act_window",
            name: "Lead List",
            res_model: "crm.lead",
            view_mode: "list",
            views: [[false, "list"]],
            target: "current",
            domain: [['type', '=', 'lead'], ['create_date', '>=', result.start_date]],
        });
        }
        else{
            this.action.doAction({
            type: "ir.actions.act_window",
            name: "Lead List",
            res_model: "crm.lead",
            view_mode: "list",
            views: [[false, "list"]],
            target: "current",
            domain: [['type', '=', 'lead'], ['create_date', '>=', result.start_date],['create_uid','=',result.user_id]],
        });
        }

    }
}


CrmDashboard.template = "crm_dashboard.CrmDashboard";
// Register the component with the action tag,
actionRegistry.add("crm_dashboard_tag", CrmDashboard);