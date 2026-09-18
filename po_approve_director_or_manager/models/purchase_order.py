# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(
        selection_add=[('approve_by_manager', 'Approved by manager'), ('approve_by_director', 'Approved by director')])
    is_activity_done = fields.Boolean(default=False, string="Activity Done", compute="_compute_is_done")

    def button_confirm(self):
        '''button_confirm'''
        for rec in self:
            print("click")
            if 50000 < rec.amount_total < 500000 and not self.env.user.has_group("purchase.group_purchase_manager"):
                rec.write({
                    'state': "approve_by_manager",
                })

                manager_grp = self.env.ref("purchase.group_purchase_manager")
                print("manager", manager_grp)
                manager = self.env['res.users'].search([('group_ids', '=', manager_grp.id)], limit=1)
                print("user manager", manager.partner_id.name)
                print("manager id", manager)

                activity_type = self.env.ref('mail.mail_activity_data_todo')
                activity=self.env['mail.activity'].sudo().create({
                    'activity_type_id': activity_type.id,
                    'res_model_id': self.env['ir.model']._get_id('purchase.order'),
                    'res_id': rec.id,
                    'user_id': manager.id,
                    'date_deadline': fields.Date.today() + timedelta(days=2),
                    'summary': 'Manager Please Approve the PO %s' % rec.name,
                    'unique_name': "Unique123"
                })

            elif rec.amount_total > 500000 and not self.env.user.has_group(
                    'po_approve_director_or_manager.group_director_purchase'):
                rec.write({
                    'state': "approve_by_director",
                })
                director_group = self.env.ref('po_approve_director_or_manager.group_director_purchase')
                print("director", director_group)
                director_id = self.env['res.users'].search([('group_ids', '=', director_group.id)], limit=1)
                print("director_id", director_id)

                activity_type = self.env.ref('mail.mail_activity_data_todo')
                activity = self.env['mail.activity'].sudo().create({
                    'activity_type_id': activity_type.id,
                    'res_model_id': self.env['ir.model']._get_id('purchase.order'),
                    'res_id': rec.id,
                    'user_id': director_id.id,
                    'date_deadline': fields.Date.today() + timedelta(days=2),
                    'summary': 'Director Please Approve the PO %s' % rec.name,
                    'unique_name' : "Unique123"
                })

            else:
                rec.button_approve()

    def _compute_is_done(self):
        print("compute is_done")
        for rec in self:

            planned = rec.activity_ids.filtered(lambda l:l.unique_name)
            print("planned", planned)
            activities = self.env['mail.activity'].search([('res_id','=',rec.id),('active','=','false'),('unique_name','=',"Unique123")])
            print(activities)
            if not planned:
                if activities:
                    rec.is_activity_done = True
                else:
                    rec.is_activity_done = False
            else:
                rec.is_activity_done = False

            print(rec.is_activity_done)
