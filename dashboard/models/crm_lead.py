from odoo import models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_tiles_data(self):
        company_id = self.env.company
        user_id = self.env.user.id
        print("user_id", user_id, "company_id", company_id)
        manager_grp = self.env.user.has_group('sales_team.group_sale_manager')
        print("manager", manager_grp)

        manager_rec = self.env.ref('sales_team.group_sale_manager')
        print("manager", manager_rec)

        manager = self.env['res.users'].search([('group_ids', '=', manager_rec.id)])
        print("user manager", manager.partner_id.name)

        if manager_grp:
            leads = self.search([('company_id', '=', company_id.id)])
        else:
            leads = self.search([('company_id', '=', company_id.id),
                                 ('user_id', '=', user_id)])
        print("leads", leads)
        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
        currency = company_id.currency_id.symbol
        expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
        user = self.env.user
        print(user.name, "user")

        if manager_grp:
            invoiced = self.env['account.move'].search(
                [('state', '=', 'posted'), ('move_type', '=', 'out_invoice'),
                 ('company_id', '=', company_id.id)])
            print("invoicedd", invoiced)
        else:
            invoiced = self.env['account.move'].search(
                [('state', '=', 'posted'), ('move_type', '=', 'out_invoice'), ('user_id', '=', user),
                 ('company_id', '=', company_id.id)])
            print("invoicedd", invoiced)
        list_amount = invoiced.mapped('amount_total')
        print("list_amount", list_amount)
        amount_invoiced = sum(invoiced.mapped('amount_total'))
        print("amount_invoiced", amount_invoiced)

        if manager_grp:
            won_oppurtunity = self.search(
                [('won_status', '=', 'won'), ('company_id', '=', company_id.id)])
            print("won_oppurtunity", won_oppurtunity)

            lost_oppurtunity = self.search(
                [('company_id', '=', company_id.id), ('user_id', '=', user.id), ('won_status', '=', 'lost'),
                 ('active', '=', 'false')])
            print("loss_revenue", lost_oppurtunity)
        else:
            won_oppurtunity = self.search(
                [('won_status', '=', 'won'), ('company_id', '=', company_id.id), ('user_id', '=', user.id)])
            print("won_oppurtunity", won_oppurtunity)

            lost_oppurtunity = self.search(
                [('company_id', '=', company_id.id), ('user_id', '=', user.id), ('won_status', '=', 'lost'),
                 ('active', '=', 'false')])
            print("loss_revenue", lost_oppurtunity)

        won_revenue = sum(won_oppurtunity.mapped('expected_revenue'))
        print("won_revenue", won_revenue)

        lost_revenue = sum(lost_oppurtunity.mapped('expected_revenue'))
        print("lost_revenue", lost_revenue)

        total_loss_won = lost_revenue + won_revenue
        print("total_loss_won", total_loss_won)

        win_ratio = (won_revenue / total_loss_won)
        win_ratio = round(win_ratio, 2)
        print("win_ratio", win_ratio)

        return {
            'total_leads': len(my_leads),
            'total_opportunity': len(my_opportunity),
            'expected_revenue': expected_revenue,
            'currency': currency,
            'amount_invoiced': amount_invoiced,
            'won_revenue': won_revenue,
            'lost_revenue': lost_revenue,
            'win_ratio': win_ratio,
            'user_id': user_id,
            'company_id': company_id,
        }

    @api.model
    def get_lost_data(self):

        manager_grp = self.env.user.has_group('sales_team.group_sale_manager')
        print("manager", manager_grp)

        manager_rec = self.env.ref('sales_team.group_sale_manager')
        print("manager", manager_rec)

        manager = self.env['res.users'].search([('group_ids', '=', manager_rec.id)])
        print("user manager", manager.partner_id.name)

        print("ghjk")
        company_id = self.env.company
        print("company_id", company_id)
        user = self.env.user

        if manager:
            lost_oppurtunity = self.search(
                [('company_id', '=', company_id.id), ('won_status', '=', 'lost'),
                 ('active', '=', 'false')])
            print("lost_oppurtunity", lost_oppurtunity)
        else:
            lost_oppurtunity = self.search(
                [('company_id', '=', company_id.id), ('user_id', '=', user.id), ('won_status', '=', 'lost'),
                 ('active', '=', 'false')])
            print("lost_oppurtunity", lost_oppurtunity)

        return [
            {'label': 'jan', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 1))},
            {'label': 'feb', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 2))},
            {'label': 'mar', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 3))},
            {'label': 'apr', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 4))},
            {'label': 'may', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 5))},
            {'label': 'jun', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 6))},
            {'label': 'jul', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 7))},
            {'label': 'aug', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 8))},
            {'label': 'sep', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 9))},
            {'label': 'oct', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 10))},
            {'label': 'nov', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 11))},
            {'label': 'dec', 'count': len(lost_oppurtunity.filtered(lambda x: x.date_closed.month == 12))}, ]

    @api.model
    def get_activity_data(self):
        print("activity_data")

        manager_grp = self.env.user.has_group('sales_team.group_sale_manager')
        print("manager", manager_grp)

        manager_rec = self.env.ref('sales_team.group_sale_manager')
        print("manager", manager_rec)

        manager = self.env['res.users'].search([('group_ids', '=', manager_rec.id)])
        print("user manager", manager.partner_id.name)

        company_id = self.env.company
        user_id = self.env.user
        print("company_id", company_id.name, "user_id", user_id.name)

        activities = self.env['mail.activity.type'].search([])
        for act in activities:
            print('act', act.name)

        if manager:
            activ=self.search([('activity_type_id','in',activities.ids),('company_id','=',company_id.id)])
            print("activ", activ)

        else:
            activ = self.search([('activity_type_id','=',activities.ids),('user_id','=',user_id.id)])

        print("count",len(activ.filtered(lambda x: x.activity_type_id.name=='Call')))

        return[
            {'label': 'To-DO','count' : len(activ.filtered(lambda x: x.activity_type_id.name=='T0-D0'))},
            {'label': 'Email', 'count': len(activ.filtered(lambda x: x.activity_type_id.name=='Email'))},
            {'label': 'Call', 'count': len(activ.filtered(lambda x: x.activity_type_id.name == 'Call'))},
            {'label': 'Meeting', 'count': len(activ.filtered(lambda x: x.activity_type_id.name == 'Meeting'))},
            {'label': 'Document', 'count': len(activ.filtered(lambda x: x.activity_type_id.name == 'Document'))},
        ]

    @api.model
    def get_medium_data(self):
        print("medium_data")
        company_id = self.env.company
        user_id = self.env.user
        manager_rec = self.env.ref('sales_team.group_sale_manager')
        print("manager", manager_rec)
        manager = self.env['res.users'].search([('group_ids', '=', manager_rec.id)])
        print("user manager", manager.partner_id.name)

        mediums = self.env['utm.medium'].search([])
        print("mediums", mediums)
        for medium in mediums:
            print(medium.name)
        if manager:
            lead_medium = self.search([('medium_id','in',mediums.ids),('company_id','=',company_id.id)])
        else:
            lead_medium = self.search([('medium_id','in',mediums.ids),('company_id','=',company_id.id),('user_id','=',user_id.id)])
            print("lead_medium", lead_medium)


        return [
            {'medium':'Banner','count' : len(lead_medium.filtered(lambda x: x.medium_id.name == 'Banner'))},
            {'medium': 'Direct', 'count': len(lead_medium.filtered(lambda x: x.medium_id.name == 'Direct'))},
            {'medium':'Email', 'count': len(lead_medium.filtered(lambda x: x.medium_id.name == 'Email'))},
            {'medium':'Facebook','count':len(lead_medium.filtered(lambda x: x.medium_id.name == 'Facebook'))},
            {'medium':'Google Adwords', 'count': len(lead_medium.filtered(lambda x: x.medium_id.name == 'Google Adwords'))},
            {'medium':'LinkedIn','count': len(lead_medium.filtered(lambda x: x.medium_id.name == 'LinkedIn'))},
            {'medium':'Phone','count': len(lead_medium.filtered(lambda x: x.medium_id.name == 'Phone'))},
            {'medium':'Television','count': len(lead_medium.filtered(lambda x: x.medium_id.name == 'Television'))},
            {'medium': 'Website','count': len(lead_medium.filtered(lambda x: x.medium_id.name == 'Website'))},
            {'medium': 'X',
             'count': len(lead_medium.filtered(lambda x: x.medium_id.name == 'x'))},
        ]

    @api.model
    def get_campaign_data(self):
        print("campaign_data")
        company_id = self.env.company
        user_id = self.env.user
        manager_rec = self.env.ref('sales_team.group_sale_manager')
        print("manager", manager_rec)
        manager = self.env['res.users'].search([('group_ids', '=', manager_rec.id)])
        print("user manager", manager.partner_id.name)

        campaigns = self.env['utm.campaign'].search([])
        for campaign in campaigns:
            print("campaign", campaign.title)
        if manager:
            lead_campaign = self.search([('campaign_id','in',campaigns.ids),('company_id','=',company_id.id)])
            print("lead_campaign", lead_campaign)
        else:
            lead_campaign = self.search([('campaign_id','in',campaigns.ids),('company_id','=',company_id.id),('user_id','=',user_id.id)])
        return [
            {'campaign':'Sale' , 'count':len(lead_campaign.filtered(lambda x: x.campaign_id.name == 'Sale'))},
            {'campaign':'Christmas Special', 'count':len(lead_campaign.filtered(lambda x: x.campaign_id.name == 'Christmas Special'))},
            {'campaign':'Email Campaign - Services', 'count': len(lead_campaign.filtered(lambda x: x.campaign_id.name == 'Email Campaign - Services'))},
            {'campaign':'Email Campaign - Products', 'count' : len(lead_campaign.filtered(lambda x: x.campaign_id.name == 'Email Campaign - Products'))},
        ]

    @api.model
    def get_lead_month_data(self):
        print("lead_month_data")
        company_id = self.env.company
        user_id = self.env.user
        manager_rec = self.env.ref('sales_team.group_sale_manager')
        print("manager", manager_rec)
        manager = self.env['res.users'].search([('group_ids', '=', manager_rec.id)])
        print("user manager", manager.partner_id.name)

        if manager:
            months = self.search([('company_id','=',company_id.id),("type",'=','lead')])
            print("months", months)
        else:
            months = self.search([('company_id','=',company_id.id),('user_id','=',user_id.id),("type",'=','lead')])
        return [
            {'label': 'jan', 'count': len(months.filtered(lambda x: x.create_date.month == 1))},
            {'label': 'feb', 'count': len(months.filtered(lambda x: x.create_date.month == 2))},
            {'label': 'mar', 'count': len(months.filtered(lambda x: x.create_date.month == 3))},
            {'label': 'apr', 'count': len(months.filtered(lambda x: x.create_date.month == 4))},
            {'label': 'may', 'count': len(months.filtered(lambda x: x.create_date.month == 5))},
            {'label': 'jun', 'count': len(months.filtered(lambda x: x.create_date.month == 6))},
            {'label': 'jul', 'count': len(months.filtered(lambda x: x.create_date.month == 7))},
            {'label': 'aug', 'count': len(months.filtered(lambda x: x.create_date.month == 8))},
            {'label': 'sep', 'count': len(months.filtered(lambda x: x.create_date.month == 9))},
            {'label': 'oct', 'count': len(months.filtered(lambda x: x.create_date.month == 10))},
            {'label': 'nov', 'count': len(months.filtered(lambda x: x.create_date.month == 11))},
            {'label': 'dec', 'count': len(months.filtered(lambda x: x.create_date.month == 12))},
        ]






