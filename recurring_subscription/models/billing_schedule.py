# -*- coding: utf-8 -*-
from odoo import fields, models,api

class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing Schedule'
    _rec_name = ('period')
    _inherit = ['mail.thread']

    is_simulation = fields.Boolean(string='Is Simulation?')
    names = fields.Char(string="Bill Name",required=True)
    period = fields.Date(string='Period', required=True)
    restrict_customers_ids = fields.Many2many('res.partner',string='Restrict Customers',required=True)

    active = fields.Boolean(string='Active')
    subscription_ids = fields.Many2many("recurring.subscription", string="Recurring Subscription",required=True)
    subscription_count = fields.Integer(string="Subscription Count")
    credit_rec_ids = fields.One2many('recurring.credit','recurring_sub_id',
                                      string='Recurring Credits')
    total_credits = fields.Float(string="Total Credits")
    subscription_count = fields.Integer(string="Subscription Count" , compute='_compute_subscription_count')


    @api.depends('subscription_ids')
    def _compute_subscription_count(self):
        '''compute subscription count'''
        for rec in self:
            rec.subscription_count = len(rec.subscription_ids)

    def action_view_subscription(self):
        '''button action for recurring subscription smart tab'''
        for rec in self:
            if rec.subscription_ids:
                return{
                    'type': 'ir.actions.act_window',
                    'name': 'Subscriptions',
                    'res_model': 'recurring.subscription',
                    'view_mode': 'list,form',
                    'domain' : [('id','in',self.subscription_ids.ids)],}

