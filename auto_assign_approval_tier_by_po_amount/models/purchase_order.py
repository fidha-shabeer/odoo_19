# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(
        selection_add=[('approve_by_manager', 'Approved by manager'), ('approve_by_director', 'Approved by director')])
    is_activity_done = fields.Boolean(default=False,string="Activity Not Done",compute="_compute_is_activity_done")

    def button_confirm(self):
        '''button_confirm'''
        for rec in self:
            print("click")
            if rec.amount_total >= 50000 and rec.amount_total < 500000:
                if not self.env.user.has_group('purchase.group_purchase_manager') :
                    rec.write({
                        'state': "approve_by_manager"
                    })
                    manager_grp = self.env.ref("purchase.group_purchase_manager")
                    print("manager", manager_grp)
                    manager = self.env['res.users'].search([('group_ids', '=', manager_grp.id)], limit=1)
                    print("user manager", manager.partner_id.name)
                    print("manager id", manager)

                    activity_type = self.env.ref('mail.mail_activity_data_todo')
                    self.env['mail.activity'].sudo().create({
                        'activity_type_id': activity_type.id,
                        'res_model_id': self.env['ir.model']._get_id('purchase.order'),
                        'res_id': rec.id,
                        'user_id': manager.id,
                        'date_deadline': fields.Date.today() + timedelta(days=2),
                        'summary': 'Manager Please Approve the PO %s' % rec.name,
                    })


            if rec.amount_total > 500000 and not self.env.user.has_group('auto_assign_approval_tier_by_po_amount.group_director_purchase'):
                rec.write({
                    'state': "approve_by_director",
                })

                director_group = self.env.ref('auto_assign_approval_tier_by_po_amount.group_director_purchase')
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
                })

            rec.button_approve()

        return super().button_confirm()

    def action_approve(self):
        '''action_approve'''
        print("action_approve")
        for rec in self:
            print("total", rec.amount_total)
            if rec.amount_total >= 50000 and rec.amount_total < 500000:
                if self.env.user.has_group("purchase.group_purchase_manager"):
                    print("manager")
                    rec.write({
                        'state' : "purchase",
                    })
                else:
                    rec.write({
                        'state': "approve_by_manager",
                    })

                    manager_grp = self.env.ref("purchase.group_purchase_manager")
                    print("manager", manager_grp)
                    manager = self.env['res.users'].search([('group_ids', '=', manager_grp.id)], limit=1)
                    print("user manager", manager.partner_id.name)
                    print("manager id", manager)

                    activity_type = self.env.ref('mail.mail_activity_data_todo')
                    self.env['mail.activity'].sudo().create({
                        'activity_type_id': activity_type.id,
                        'res_model_id': self.env['ir.model']._get_id('purchase.order'),
                        'res_id': rec.id,
                        'user_id': manager.id,
                        'date_deadline': fields.Date.today() + timedelta(days=2),
                        'summary': 'Manager Please Approve the PO %s' % rec.name,
                    })

            if rec.amount_total > 500000:
                if not self.env.user.has_group("auto_assign_approval_tier_by_po_amount.group_director_purchase"):
                    print("not director")
                    rec.write({
                        'state': "approve_by_director",
                    })
                    director_group = self.env.ref('auto_assign_approval_tier_by_po_amount.group_director_purchase')
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
                    })
                else:
                    rec.write({
                        'state': "purchase",
                    })




    def _compute_is_activity_done(self):
        '''compute activity done status'''
        print("_compute_is_activity_done")
        for rec in self:
            if rec.activity_state != 'planned':
                rec.is_activity_done = True
            else:
                rec.is_activity_done = False

    # def action_by_manager(self):
    #     for rec in self:
    #         rec.write({
    #             'state': "purchase",
    #         })
    #
    # def action_by_director(self):
    #     for rec in self:
    #         rec.write({
    #             'state': "purchase",
    #         })



