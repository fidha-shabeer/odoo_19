# -*- coding: utf-8 -*-
from odoo import fields,models,api

class PosSession(models.Model):
    _inherit = 'pos.session'

    max_discount_limit = fields.Float(string="Maximum Discount Limit",compute="_compute_max_discount_limit")
    current_total_discount = fields.Float(string="Current Total Discount",compute="_compute_current_discount")

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

    def _compute_current_discount(self):
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

        # discounts = order.mapped('discount')
        # print("discounts", discounts)
        # sum_discounts = sum(discounts)
        # print("sum_discounts", sum_discounts)

        for rec in self:
            rec.current_total_discount = amount



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

