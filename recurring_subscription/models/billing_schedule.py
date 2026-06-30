# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo import Command

class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing Schedule'
    _rec_name = ('period')
    _inherit = ['mail.thread']

    is_simulation = fields.Boolean(string='Is Simulation?')
    names = fields.Char(string="Bill Name")
    period = fields.Date(string='Period')
    restrict_customers_ids = fields.Many2many('res.partner',string='Restrict Customers',required=True)
    # credit_rec_ids = fields.Many2many('recurring.credit', related ='subscription_ids.credit_ids')
    total_credits = fields.Float()

    active = fields.Boolean(string='Active', default=True)
    subscription_ids = fields.Many2many("recurring.subscription", string="Recurring Subscription",required=True)


    credit_rec_ids = fields.Many2many('recurring.credit',string="Recurring Credits")


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

    @api.onchange('subscription_ids')
    def _onchange_subscription_ids(self):
        self.update({'restrict_customers_ids': [(fields.Command.set(self.subscription_ids.mapped('partner_id').ids))],
                     'credit_rec_ids' : [(fields.Command.set(self.subscription_ids.ids))]
                     })
    @api.onchange('credit_rec_ids')
    def _onchange_credit_rec_ids(self):
        for rec in self:
            if rec.credit_rec_ids:
                rec.total_credits = sum(rec.credit_rec_ids.mapped('credit_amounts'))

    def action_billing(self):
        print(123, self.id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Billing Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'target': 'new',
            # 'context': {'active_ids': self.ids},
        }
