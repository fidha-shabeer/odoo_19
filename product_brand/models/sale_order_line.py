# -*- coding: utf-8 -*-
from odoo import models,fields,api
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    brand = fields.Char(string="Brand")

    @api.onchange("product_template_id")
    def _onchange_product_template_id(self):
        if self.product_template_id:
            self.brand = self.product_template_id.product_brand



