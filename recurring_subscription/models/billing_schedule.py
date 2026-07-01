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
    # credit_rec_ids = fields.Many2many('recurring.credit', related ='subscription_ids.credit_ids')
    total_credits = fields.Float()

    active = fields.Boolean(string='Active', default=True)
    subscription_ids = fields.Many2many("recurring.subscription", string="Recurring Subscription",required=True)


    credit_rec_ids = fields.Many2many('recurring.credit',string="Recurring Credits")


    total_credits = fields.Float(string="Total Credits")
    subscription_count = fields.Integer(string="Subscription Count" , compute='_compute_subscription_count')

    invoice_count = fields.Integer(string="Invoice Count" , compute='_compute_invoice_count')


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
                     'credit_rec_ids' : [(fields.Command.set(self.subscription_ids.ids))],
                     })
    @api.onchange('credit_rec_ids')
    def _onchange_credit_rec_ids(self):
        for rec in self:
            if rec.credit_rec_ids:
                rec.total_credits = sum(rec.credit_rec_ids.mapped('credit_amounts'))

    def action_billing(self):
        for r in self:
            if r.subscription_ids:
                subscriptions = self.subscription_ids.filtered(lambda r: r.status=='confirm')

                for rec in subscriptions:
                    credit =  self.credit_rec_ids.filtered(lambda c:c.credit_amounts == rec.recurring_amount)
                    if not credit:
                        credit = self.credit_rec_ids.filtered(lambda c:c.credit_amounts <= rec.recurring_amount)[:1]

                    final_amount =  rec.recurring_amount - credit.credit_amounts

                    invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': rec.partner_id.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': [(0, 0, {
                        'product_id': rec.product_id.id,
                        'quantity': 1,
                        'price_unit': final_amount,
                        })],
                })

        self.write({'active':False})

    def auto_invoice(self):
        auto_create = self.subscription_ids.search([('status','=','confirm'),('due_dates','<',fields.Date.today())])

        for rec in auto_create:
            credit = self.credit_rec_ids.filtered(
                lambda c: c.credit_amounts == rec.recurring_amount)
            if not credit:
                credit = self.credit_rec_ids.filtered(
                    lambda c: c.credit_amounts <= rec.recurring_amount)[:1]

            final_amount = rec.recurring_amount - credit.credit_amounts

            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec.partner_id.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                    'product_id': rec.product_id.id,
                    'quantity': 1,
                    'price_unit': final_amount,
                })],
            })


    # def action_view_invoice(self):
    #     '''button action for invoice'''
    #     for rec in self:
    #             return {
    #                 'type': 'ir.actions.act_window',
    #                 'name': 'Invoice',
    #                 'res_model': 'account.move',
    #                 'view_mode': 'list,form',
    #                 'domain': [('invoice', 'in', rec.id)], }
