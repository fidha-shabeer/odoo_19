# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def archive_product(self):
        """ Archive Product """
        print("dfghjk")
        date_filter = fields.Datetime.now() - timedelta(days=5)
        print("sdfghjkl",date_filter)
        product = self.env["product.product"].search([('active','=',True)])
        print("sdfghjkl",product)
        record_filter = self.env['sale.report'].search([('date','<=',date_filter),('state','=','sale'),])

        product_filter = record_filter.mapped("product_id")
        for line in product_filter:
            line.write({'active': False})
        print("sdfghjkl",product_filter)






