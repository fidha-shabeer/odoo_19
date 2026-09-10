# -*- coding: utf-8 -*-
from operator import contains
from os import WCONTINUED

from odoo import fields,models,api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id','product_uom_qty')
    def _onchange_product_id(self):
        print("changing onchange")

        price = self.env['product.pricing.notebook'].search([('partner_id','=',self.order_id.partner_id.id),('product_id','=',self.product_id),('min_qty','<=',self.product_uom_qty)],order='min_qty desc',limit=1)
        search = price.mapped('unit_price')
        print("price",price)
        print("search",search)

        self.price_unit = price.unit_price
        print("unit_price", self.price_unit)




