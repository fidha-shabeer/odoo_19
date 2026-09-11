# -*- coding: utf-8 -*-
from odoo import fields, models,api

class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_template_id")
    def _onchange_product_template_id(self):
        if self.product_template_id:
            self.discount = self.order_id.discount_percent
        else:
            self.discount = 0.0

