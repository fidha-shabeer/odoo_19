from odoo import models, api

class CrmLead(models.Model):
   _inherit = 'crm.lead'
   @api.model
   def get_tiles_data(self):
       company_id = self.env.company
       user_id =  self.env.user.id
       print("user_id",user_id,"company_id",company_id)
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
                            ('user_id', '=', self.env.user.id)])
       my_leads = leads.filtered(lambda r: r.type == 'lead')
       my_opportunity = leads.filtered(lambda r: r.type == 'opportunity')
       currency = company_id.currency_id.symbol
       expected_revenue = sum(my_opportunity.mapped('expected_revenue'))
       user = self.env.user
       print(user.name,"user")

       if manager_grp:
           invoiced = self.env['account.move'].search(
               [('state', '=', 'posted'), ('move_type', '=', 'out_invoice'),
                ('company_id', '=', company_id.id)])
           print("invoicedd", invoiced)
       else:
           invoiced = self.env['account.move'].search([('state','=','posted'),('move_type','=','out_invoice'),('user_id','=',user),('company_id','=',company_id.id)])
           print("invoicedd",invoiced)
       list_amount = invoiced.mapped('amount_total')
       print("list_amount",list_amount)
       amount_invoiced = sum(invoiced.mapped('amount_total'))
       print("amount_invoiced",amount_invoiced)


       if manager_grp:
           won_oppurtunity = self.search(
               [('won_status', '=', 'won'), ('company_id', '=', company_id.id)])
           print("won_oppurtunity", won_oppurtunity)

           lost_oppurtunity = self.search(
               [('company_id', '=', company_id.id), ('user_id', '=', user.id), ('won_status', '=', 'lost'),
                ('active', '=', 'false')])
           print("loss_revenue", lost_oppurtunity)
       else:
            won_oppurtunity = self.search([('won_status','=','won'),('company_id','=',company_id.id),('user_id','=',user.id)])
            print("won_oppurtunity",won_oppurtunity)

            lost_oppurtunity = self.search(
                [('company_id', '=', company_id.id), ('user_id', '=', user.id), ('won_status', '=', 'lost'),
                 ('active', '=', 'false')])
            print("loss_revenue", lost_oppurtunity)

       won_revenue = sum(won_oppurtunity.mapped('expected_revenue'))
       print("won_revenue",won_revenue)

       lost_revenue = sum(lost_oppurtunity.mapped('expected_revenue'))
       print("lost_revenue",lost_revenue)

       total_loss_won = lost_revenue + won_revenue
       print("total_loss_won",total_loss_won)

       win_ratio = (won_revenue / total_loss_won)
       win_ratio = round(win_ratio,2)
       print("win_ratio",win_ratio)


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