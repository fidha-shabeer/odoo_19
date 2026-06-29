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
    restrict_customers_ids = fields.Many2many('res.partner',string='Restrict Customers',required=True,compute= 'compute_restrict_customers_ids')

    active = fields.Boolean(string='Active', default=True)
    subscription_ids = fields.Many2many("recurring.subscription", string="Recurring Subscription",required=True)
    subscription_count = fields.Integer(string="Subscription Count")
    credit_rec_ids = fields.Many2many('recurring.credit',compute='_compute_credits')

    total_credits = fields.Float(string="Total Credits", compute = '_compute_total_credits')
    subscription_count = fields.Integer(string="Subscription Count" , compute='_compute_subscription_count')

    confirm_filter = fields.Many2many('recurring.subscription', string="Confirm Filter",compute='_compute_confirm_filter')
    confirm_credit = fields.Many2one('recurring.credit', compute='_compute_credits_filter')

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

    @api.depends('subscription_ids')
    def compute_restrict_customers_ids(self):
        for rec in self:
            rec.restrict_customers_ids = rec.subscription_ids.mapped('partner_id')

    @api.depends('subscription_ids')
    def _compute_credits(self):
        for rec in self:
            rec.credit_rec_ids = rec.subscription_ids.mapped('credits_ids')

    @api.depends('credit_rec_ids')
    def _compute_credits_filter(self):
        for rec in self:
            rec.confirm_credit = rec.credit_rec_ids.filtered(
                lambda r: r.state == 'fully approved')


    @api.depends('subscription_ids')
    def _compute_confirm_filter(self):
        for rec in self:
            rec.confirm_filter = rec.subscription_ids.filtered(lambda r: r.status == 'confirm')


    @api.depends('confirm_filter.credits_ids.credit_amounts')
    def _compute_total_credits(self):
        for rec in self:
            rec.total_credits = sum(rec.confirm_filter.mapped('credits_ids.credit_amounts'))

