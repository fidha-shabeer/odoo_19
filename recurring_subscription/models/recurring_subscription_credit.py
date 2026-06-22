# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.exceptions import ValidationError


class RecurringSubscriptionCredit(models.Model):
    """ Recurring Subscription credit"""
    _name="recurring.credit"
    _description = "Recurring Subscription Credit"
    _rec_name = "recurring_sub_id"
    _inherit = ['mail.thread']

    recurring_sub_id=fields.Many2one("recurring.subscription",string="Recurring Subscription",required=True)
    id_establishment=fields.Char(string="Establishment Id" , related= "recurring_sub_id.id_establishment")
    due_date = fields.Date(string="Due Date", related= "recurring_sub_id.due_dates")
    # partner_id = fields.Many2one("res.partner",string="Recurring Subscription Partner",tracking=True, required=True)
    partner_id =  fields.Many2one(string="Patner",related= "recurring_sub_id.partner_id")
    recurring_amounts = fields.Monetary(string="Recurring Amount",related= "recurring_sub_id.recurring_amount")
    credit_amounts = fields.Monetary(string="Credit Amount",required=True,currency_field="currency_id")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')

    state = fields.Selection(selection=[('pending', 'Pending'), ('confirmed', 'Confirmed'),
                                        ('first approved', 'First Approved'),( 'fully approved','Fully Approved'),('rejected', 'Rejected')],tracking=True)
    date_begin = fields.Datetime(string="Date Begin")
    date_end = fields.Datetime(string="Date End")


    @api.onchange('credit_amounts')
    def onchange_recurrent_sub_id(self):
        """ Onchange method for Recurring Subscription Credit """
        for rec in self:
            if rec.recurring_sub_id and (rec.credit_amounts == 0 or rec.credit_amounts >= rec.recurring_sub_id.recurring_amount):
                rec.recurring_sub_id = False

    @api.constrains('credit_amounts')
    def check_credit_amounts(self):
        """validation for credit amounts"""
        for rec in self:
            if rec.credit_amounts==0:
                raise ValidationError("Credit Amounts cannot be zero")
