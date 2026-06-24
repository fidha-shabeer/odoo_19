# -*- coding: utf-8 -*-
from odoo import fields, models,api

class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing Schedule'
    _rec_name = ('period')
    _inherit = ['mail.thread']

    simulation = fields.Boolean(string='Simulation')
    period = fields.Date(string='Period')
    restrict_customers_id = fields.Many2many('res.partner',string='Restrict Customers',required=True)
    active = fields.Boolean(string='Active')
    subscription_id = fields.Many2many("recurring.subscription", string="Recurring Subscription",required=True)
    total_credits = fields.Float(string="Total Credits")
    # subs_id = fields.One2many('recurring.subscription','billing_schedule_id',string="Subscriptions")
    subscription_count = fields.Integer(string="Subscription Count" , compute='_compute_subscription_count')


    @api.depends('subscription_id')
    def _compute_subscription_count(self):
        for rec in self:
            rec.subscription_count = len(rec.subscription_id)

    def action_view_subscription(self):
        print(9,self.subscription_id.id)
        return{
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'res_model': 'recurring.subscription',
            'view_mode': 'list,form',
            'domain' : [('id','in',self.subscription_id.ids)],
        }

