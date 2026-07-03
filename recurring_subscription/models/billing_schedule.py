# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo import Command
from odoo.exceptions import ValidationError

class BillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing Schedule'
    _rec_name = ('period')
    _inherit = ['mail.thread']

    is_simulation = fields.Boolean(string='Is Simulation?')
    names = fields.Char(string="Bill Name")
    period = fields.Date(string='Period')
    restrict_customers_ids = fields.Many2many('res.partner',string='Restrict Customers',required=True)


    invoice_ids = fields.One2many('account.move','billing', string='Invoices')
    invoice_count = fields.Integer(string="Invoice Count", compute='_compute_invoice_count')

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

    @api.depends('subscription_ids')
    def _compute_invoice_count(self):
        '''compute subscription count'''
        for rec in self:
            rec.invoice_count = len(rec.subscription_ids)

    def action_view_subscription(self):
        '''button action for recurring subscription smart tab'''
        for rec in self:
            if rec.subscription_ids:
                return{
                    'type': 'ir.actions.act_window',
                    'name': 'Subscriptions',
                    'res_model': 'recurring.subscription',
                    'view_mode': 'list,form',
                    'domain' : [('id','in',rec.subscription_ids.ids)],}

    @api.onchange('subscription_ids')
    def _onchange_subscription_ids(self):
        for rec in self:
            rec.update({'restrict_customers_ids': [(fields.Command.set(rec.subscription_ids.mapped('partner_id').ids))],
                         'credit_rec_ids' : [(fields.Command.set(rec.subscription_ids.ids))],
                         })
    @api.onchange('credit_rec_ids')
    def _onchange_credit_rec_ids(self):
        for rec in self:
            if rec.credit_rec_ids:
                rec.total_credits = sum(rec.credit_rec_ids.mapped('credit_amounts'))
            else:
                rec.total_credits = 0

    def action_billing(self):
        for r in self:
            subscriptions = r.subscription_ids.filtered(
                    lambda r: r.status == 'confirm')

            for rec in subscriptions:
                credit = self.credit_rec_ids.filtered(
                    lambda c: c.credit_amounts == rec.recurring_amount)[:1]
                if not credit:
                    credit = self.credit_rec_ids.filtered(
                        lambda c: c.credit_amounts <= rec.recurring_amount)[:1]

                final_amount = rec.recurring_amount
                credit_product = self.env['product.template'].search([('name','=','Credit Amount')])

                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': rec.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': [(fields.Command.create({
                    'product_id': rec.product_id.id,
                    'quantity': 1,
                    'price_unit': final_amount,
                        })),
                    (fields.Command.create({
                    'product_id': credit_product.id,
                    'quantity': 1,
                    'price_unit': -credit.credit_amounts,})),
                        ],
                    })

    def auto_invoice(self):
        auto_create = self.subscription_ids.search([('status','=','confirm'),('due_dates','<',fields.Date.today())])
        for r in self:
            subscriptions = r.subscription_ids.filtered(
                lambda r: r.status == 'confirm')

            for rec in subscriptions:
                credit = self.credit_rec_ids.filtered(
                    lambda c: c.credit_amounts == rec.recurring_amount)[:1]
                if not credit:
                    credit = self.credit_rec_ids.filtered(
                        lambda c: c.credit_amounts <= rec.recurring_amount)[:1]

                final_amount = rec.recurring_amount
                credit_product = self.env['product.template'].search(
                    [('name', '=', 'Credit Amount')])

                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': rec.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': [(fields.Command.create({
                        'product_id': rec.product_id.id,
                        'quantity': 1,
                        'price_unit': final_amount,
                    })),
                        (fields.Command.create({
                            'product_id': credit_product.id,
                            'quantity': 1,
                            'price_unit': -credit.credit_amounts, })),
                    ],
                })

    def action_view_invoice(self):
        '''button action for recurring subscription smart tab'''
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'res_id': 'invoice.id',
            'view_mode': 'form',
            'domain': [('id', 'in', 'invoice.id')],

        }