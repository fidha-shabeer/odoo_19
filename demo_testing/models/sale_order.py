# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    order_type = fields.Selection([
        ('normal', 'Normal'),
        ('priority', 'Priority'),
        ('urgent', 'Urgent'),
    ],
        string='Order Type',
        default='normal')

    # ref =fields.Char(string="ref")

    def action_confirm(self):
        print("demo")
        for rec in self:
            print(rec.order_type, 'type')
            if rec.order_type == 'urgent':
                if not rec.order_line:
                    raise ValidationError("the order should have ordes at least one")
                if rec.amount_total < 10000:
                    raise ValidationError("the total amount must exceeds 10000")
        return super().action_confirm()

    def action_validate_selected(self):
        print("selected records", self)
        for rec in self:
            print("type:", rec.order_type)
            print("amount", rec.amount_total)
            if rec.order_type == 'urgent':
                if not rec.order_line:
                    raise ValidationError("no orders exist")
                if rec.amount_total < 10000:
                    raise ValidationError("amount should be greater than 10000")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'All selected orders are valid.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_state(self):
        print("check", self)
        for rec in self:
            if rec.state == 'sale':
                raise ValidationError("in confirm state")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'All selected orders are in other state.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_discount(self):
        print("soon")
        for rec in self:
            print(rec.amount_total, "total")
            if rec.state == 'cancel':
                continue
            if rec.state == 'draft':
                raise ValidationError("draft state cant receive discount")
            else:
                if rec.amount_total > 10000:
                    for line in rec.order_line:
                        line.write({
                            'discount': 5,
                        })
                else:
                    raise ValidationError("total amount should exceeds 10000")

        return True

    def action_customer(self):
        print("customer", self)
        confirmed = self.search([('state','=','sale')])
        for order in confirmed:
            print("order name",order.name)
            print("total",order.amount_total)

        # confirmed = self.filtered(lambda l: l.state == 'sale')
        customer = confirmed.mapped('partner_id.name')
        if not confirmed:
            raise ValidationError("no confirmed orders")

        print("confirm", confirmed)

        print("customer", customer)

        # @api.model_create_multi
        # def create(self, vals_list):
        #     for vals in vals_list:
        #         if vals.get('ref', 'New') == 'New':
        #             vals['ref'] = self.env['ir.sequence'].next_by_code(
        #                 'refsequence'
        #             )
        #
        #     return super().create(vals_list)




