# -*- coding: utf-8 -*-
from odoo import fields, models,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount = fields.Float(string="Vip Discount")
    discount_percent = fields.Float(string="Vip Discount %")

    @api.onchange("partner_id")
    def _onchange_discount(self):
        if self.partner_id.is_vip:
            self.discount = self.partner_id.vip_discount
        else:
            self.discount = 0.0

    @api.onchange("partner_id")
    def _onchange_discount_percent(self):
        if self.partner_id.is_vip:
            # self.discount_percent =self.order_line.price_unit - self.partner_id.vip_discount
            dicount_difference = self.order_line.price_unit - self.partner_id.vip_discount
            self.discount_percent = (dicount_difference / self.order_line.price_unit)*100
        else:
            self.discount_percent = 0.0

        for l in self.order_line:
                l.discount = self.discount_percent