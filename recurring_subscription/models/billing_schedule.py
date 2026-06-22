# -*- coding: utf-8 -*-
from odoo import fields, models


class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing Schedule'
    _rec_name = ('from_date')
    _inherit = ['mail.thread']

    simulation = fields.Boolean(string='Simulation')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    restrict_customers_id = fields.Many2many('res.partner',string='Restrict Customers',required=True)
    active = fields.Boolean(string='Active')
    subscription_id = fields.Many2many("recurring.subscription", string="Recurring Subscription",required=True)
    total_credits = fields.Float(string="Total Credits")


