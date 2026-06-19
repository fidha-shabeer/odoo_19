# -*- coding: utf-8 -*-
from odoo import fields, models

class RecurringSubscriptionCredit(models.Model):
    """ Recurring Subscription credit"""
    _name="recurring.credit"
    _description = "Recurring Subscription Credit"
    _rec_name = "recurring_sub_id"
    _inherit = ['mail.thread']

    recurring_sub_id=fields.Many2one("recurring.subscription",string="Recurring Subscription",required=True)
    establishment_id=fields.Char(string="Establishment Id")
    due_date = fields.Date(string="Due Date")
    partner_id = fields.Many2one("res.partner",string="Recurring Subscription Partner",tracking=True, required=True)
    companys_id = fields.Many2one("res.company", string="Company", )
    credit_amounts = fields.Monetary(string="Credit Amount",required=True,currency_field="currency_id",digits=(12,2))
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')

    state = fields.Selection(selection=[('pending', 'Pending'), ('confirmed', 'Confirmed'),('first approved', 'First Approved'),( 'fully approved','Fully Approved'),('rejected', 'Rejected')])
    date_begin = fields.Datetime(string="Date Begin")
    date_end = fields.Datetime(string="Date End")
