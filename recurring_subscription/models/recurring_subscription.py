# -*- coding: utf-8 -*-
import re

from odoo import fields,models,api,_
from datetime import timedelta
from odoo.exceptions import ValidationError

class RecurringSubscription(models.Model):
    """Recurring Subscription"""
    _name = "recurring.subscription"
    _description = "Recurring Subscription"
    _rec_name = "order_seq"
    _inherit = ['mail.thread']

    status = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'),
                                         ('done', 'Done'), ('cancel', 'Cancel')],
                              string="State",default='draft',tracking=True)
    order_seq=fields.Char(default="New")
    establishment_id = fields.Char(string="Establishment ID",required=True)
    date = fields.Date(string="Date" , required=True,tracking=True)
    due_dates=fields.Date(string="Due Dates",compute="_compute_dates" , store=True)
    next_billing = fields.Date(string="Next Bill Date", compute="_compute_next_billing",
                               store=True)
    is_leads = fields.Boolean(string="Is Lead?", required=True)
    partner_id = fields.Many2one("res.partner", string="Customer",
                                 tracking=True,required=True)
    description = fields.Text(string="Description")
    terms_condition = fields.Html(string="Terms and Condition")
    product_id = fields.Many2one("product.product", string="Product",
                                 tracking=True,required=True)
    companys_id=fields.Many2one("res.company", string="Company",)
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                    related='company_id.currency_id')

    recurring_amount = fields.Monetary(string="Recurring Amount",tracking=True,
                                    required=True,currency_field="currency_id",digits=(12,2))


    def create(self, vals_list):
        """Recurring Subscription Sequence creation    jjjj"""
        vals_list["order_seq"] = self.env["ir.sequence"].next_by_code('recsequence')
        return super(RecurringSubscription, self).create(vals_list)

    @api.depends("date")
    def _compute_dates(self):
        """Due date calculation"""
        for rec in self:
            if rec.date:
                rec.due_dates = rec.date+timedelta(days=15)
            else:
                rec.due_dates = False

    @api.depends("date")
    def _compute_next_billing(self):
        """billing date calculation"""
        for rec in self:
            if rec.date:
                rec.next_billing = rec.date+timedelta(days=30)
            else:
                rec.next_billing = False

    # @api.constrains('establishment_id')
    # def _check_establishment_id(self):
    #     for rec in self:
    #         if rec.establishment_id and not re.match(r'^(?=.*[A-Za-z]{3})(?=.*\d{3})(?=.*?[#?!@$%^&*-]{2})$', rec.establishment_id):
    #                 raise ValidationError(_("The id must contain char,int and spcl char"))

    def button_confirm(self):
        self.status='confirm'

    def button_cancel(self):
        self.status='cancel'




