# -*- coding: utf-8 -*-
from odoo import fields,models,api,_
from datetime import timedelta
from odoo.exceptions import ValidationError


class RecurringSubscription(models.Model):
    """Recurring Subscription"""
    _name = "recurring.subscription"
    _description = "Recurring Subscription"
    _rec_name = "order_seq"
    _inherit = ['mail.thread']

    status = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'),('done', 'Done'), ('cancel', 'Cancel')],
                              string="State",default='draft',tracking=True)
    order_seq=fields.Char(default="New")
    id_establishment = fields.Char(string="Establishment ID",required=True, tracking=True)
    credits_id = fields.One2many('recurring.credit','recurring_sub_id',string='Subscription Credits')
    reccuring_credit_ids = fields.Many2many("recurring.credit",string="Recurring Credits")
    billing_schedule_id = fields.Many2one("billing.schedule",string="Billing Schedule")
    date=fields.Date(string="Date",required=True,default=fields.Date.context_today)
    due_dates=fields.Date(string="Due Dates",compute="_compute_dates" , store=True)
    next_billing = fields.Date(string="Next Bill Date", compute="_compute_next_billing",
                               store=True)
    is_leads = fields.Boolean(string="Is Lead?", required=True)
    # partner_id = fields.Many2one("res.partner", string="Customer",
    #                              tracking=True,required=True)
    partner_id = fields.Many2one('res.partner',string="Customer",compute='_compute_partner_id',store=False)

    description = fields.Text(string="Description")
    terms_condition = fields.Html(string="Terms and Condition")
    product_id = fields.Many2one("product.product", string="Product",
                                 tracking=True,required=True)

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                    related='company_id.currency_id')

    recurring_amount = fields.Monetary(string="Recurring Amount",tracking=True,
                                    required=True,currency_field="currency_id")

    @api.model_create_multi
    def create(self, vals_list):
        """Recurring Subscription Sequence creation """
        for vals in vals_list:
            if vals.get('order_seq','New') == 'New':
                vals['order_seq'] = self.env["ir.sequence"].next_by_code('recsequence')
        return super(RecurringSubscription, self).create(vals_list)

    @api.depends("due_dates","credits_id.period")
    def _compute_reccuring_credits(self):
        for rec in self:
            rec.reccuring_credit_ids = (rec.credits_id.filtered
                                         (lambda r : r.period and rec.due_dates and r.period <= rec.due_dates))

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

    @api.constrains("recurring_amount")
    def _check_recurring_amount(self):
        """validation for recurring amount"""
        for rec in self:
            if rec.recurring_amount == 0:
                raise ValidationError("Recurring Amount must be greater than 0")



    # @api.constrains('establishment_id')
    # def _check_establishment_id(self):
    #     for rec in self:
    #         # if rec.establishment_id and not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",rec.establishment_id):
    #         if rec.establishment_id and not re.match(
    #                 r'^(?=.[a-zA-Z]{3,})(?=.\d{3,})'
    #                 r'(?=.*[@.#$!%?&]{2,})[A-Za-z\d@.#$!%?&]{8,}$',
    #                 rec.establishment_id):
    #             print(1234, rec.establishment_id)
    #             raise ValidationError("Recurring Amount must be greater than 0")
                # raise ValidationError(_("Invalid Format!! Id must contain char,int and spcl char."))

    

    def button_confirm(self):
        """Confirmation button """
        self.write({
            'status': 'confirm'
        })
        # self.status='confirm'

    def button_cancel(self):
        """Cancel button """
        self.write({
            'status': 'cancel'
        })
        # self.status='cancel'


    @api.depends('id_establishment')
    def _compute_partner_id(self):
        for rec in self:
            if rec.id_establishment:
                res = self.env['res.partner'].search([('id_establishments','=',rec.id_establishment)])
                if res:
                    rec.partner_id = res
                else:
                    raise ValidationError('no partner found')



