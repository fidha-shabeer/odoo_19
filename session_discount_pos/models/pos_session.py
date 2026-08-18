# -*- coding: utf-8 -*-
from odoo import fields,models,api

class PosSession(models.Model):
    _inherit = 'pos.session'

    max_discount_limit = fields.Float(string="Maximum Discount Limit",compute="_compute_max_discount_limit")
    current_total_discount = fields.Float(string="Current Total Discount",compute="_compute_current_discount",store=True)

    def get_param(self):
        params = self.env['ir.config_parameter'].sudo()
        print("params", params)
        max_discount = params.get_param(
            'session_discount_pos.max_discount_limit')
        print(max_discount,"max_discount xxxxxxxxx")

    def open_frontend_cb(self):
        print("frontend xxxxxxxxx")
        res=super().open_frontend_cb()
        params = self.env['ir.config_parameter'].sudo()
        print("params", params)
        max_discount = params.get_param(
            'session_discount_pos.max_discount_limit')
        print(max_discount, "max_discount xxxxxxxxx")
        return res


    def _compute_max_discount_limit(self):
        print("_compute_max_discount_limit")
        params = self.env['ir.config_parameter'].sudo()
        print("params", params)
        max_discount = params.get_param(
            'session_discount_pos.max_discount_limit')
        print(max_discount, "max_discount xxxxxxxxx")
        for rec in self:
            rec.max_discount_limit = max_discount
            print(rec.max_discount_limit,"max_discount xxxxxxxxx")

    @api.depends('order_ids.global_discount_amount','order_ids.discount_amount')
    def _compute_current_discount(self):
        for rec in self:
            print("_compute_current_discount")
            order = self.env['pos.order.line'].search([('order_id.session_id','=',self.id)])
            print(order)

            # am = order.get_total_discount

            amount = 0
            for line in self.env['pos.order.line'].search(
                    [('order_id', 'in', self._get_closed_orders().ids),
                    ('discount', '>', 0)]):
                amount += line._get_discount_amount()
            print(amount,"am")

            demo=self.env['pos.order.line'].search(
                [('order_id', 'in', self._get_closed_orders().ids),
                 ('discount', '>', 0)])
            print(demo,"demo")

            orders = self._get_closed_orders()
            print("orders",orders)

            sum_global = 0
            for order in orders:
                print("discount amount global : ",order.global_discount_amount)
                sum_global += order.global_discount_amount
                print("sum_global",sum_global)

            total_discount = sum_global + amount
            print("total_discount",total_discount)

            rec.current_total_discount = total_discount



    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'max discount limit' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        print("data before", data)
        data += ['max_discount_limit','current_total_discount']
        print("data after", data)
        return data

