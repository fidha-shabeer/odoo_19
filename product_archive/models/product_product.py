# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def archive_product(self):
        """ Archive Product """
        print("action started")
        date_filter = fields.Datetime.now() - timedelta(days=90)
        print("date:",date_filter)
        products = self.env["product.product"].search([('active','=',True)])
        print("active products",products)
        
        for pro in products:
            sold_filter = self.env['sale.report'].search([('product_id','=',pro.id),('state','=','sale')],order='date desc',limit=1)
            print("filtered sale",sold_filter)
            if not sold_filter:
                pro.write({'active': False})
            elif sold_filter.date < date_filter:
                pro.write({'active': False})




