# -*- coding: utf-8 -*-
from odoo import fields,models,api,_
from datetime import timedelta
from odoo.exceptions import ValidationError


class RecurringSubscription(models.Model):
    """Recurring Subscription"""
    _name = "recurring.subscription"
    _description = "Recurring Subscription"
    _rec_name = "order_seq"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    status = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'),('done', 'Done'), ('cancel', 'Cancel')],
                              string="State",default='draft',tracking=True)
    order_seq=fields.Char(default="New")
    attachment = fields.Image( attachment=True)
    id_establishment = fields.Char(string="Establishment ID",required=True, tracking=True)
    credits_ids= fields.One2many('recurring.credit','recurring_sub_id',string='Subscription Credits',compute ='_compute_recurring_credits')
    billing_schedule_id = fields.Many2one("billing.schedule",string="Billing Schedule")
    date=fields.Date(string="Date",required=True,default=fields.Date.context_today)
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

    company_id = fields.Many2one('res.company', store=True,
                                 string="Company",
                                 default=lambda
                                     self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                    related='company_id.currency_id')

    recurring_amount = fields.Monetary(string="Recurring Amount",tracking=True,
                                    required=True,currency_field="currency_id")

    total_credits = fields.Float(string="Total Credits",compute="_compute_total_credits",store =True)
    all_credit_ids = fields.One2many(comodel_name='recurring.credit',inverse_name='recurring_sub_id',string="all credits",store=True)

    @api.depends('all_credit_ids.credit_amounts','all_credit_ids.period')
    def _compute_total_credits(self):
        print("bhbhbr")
        for rec in self:
            record=rec.all_credit_ids.search([('recurring_sub_id','=',rec._origin.id), ('period','<',rec.due_dates),('state','=','fully_approved')])
            if rec.all_credit_ids:
                rec.total_credits = sum(record.mapped('credit_amounts'))
            else:
                rec.total_credits = 0

    @api.model_create_multi
    def create(self, vals_list):
        """Recurring Subscription Sequence creation """
        for vals in vals_list:
            if vals.get('order_seq','New') == 'New':
                vals['order_seq'] = self.env["ir.sequence"].next_by_code('recsequence')
        return super(RecurringSubscription, self).create(vals_list)

    @api.depends("due_dates")
    def _compute_recurring_credits(self):
        for rec in self:
            print(rec._origin.id)
            rec.credits_ids= self.env['recurring.credit'].search([
                ('recurring_sub_id','=',rec._origin.id), ('period','<',rec.due_dates),('state','=','fully_approved')])

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


    @api.onchange('id_establishment')
    def onchange_establishment(self):
        for rec in self:
            if rec.id_establishment:
                res = self.env['res.partner'].search([('id_establishments','=',rec.id_establishment)])
                if res:
                    rec.partner_id = res
                else:
                    rec.partner_id = False
                    raise ValidationError('no partner found')

    def button_confirm(self):
        """Confirmation button """
        self.write({
            'status': 'confirm'
        })


    def button_cancel(self):
        """Cancel button """
        self.write({
            'status': 'cancel'
        })



    def button_done(self):
        for rec in self:
            rec.write({
                'status': 'done'
            })
        self.action_send_mail()


    def action_send_mail(self):
        for rec in self:
            if rec.status == 'done':
                template = self.env.ref("recurring_subscription.subscription_email_template")
                email_values = {'email_from': self.env.user.email}
                template.send_mail(self.id, force_send=True,email_values=email_values)
                self.message_post(body=_("Dear customer, Your Recurring Subscription has been completed."),
                                subject='Subscription Completed',
                                message_type='email',
                                subtype_xmlid='mail.mt_comment',
                                )




