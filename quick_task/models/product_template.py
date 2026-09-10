# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self,vals):
        print("vals",vals)
        if 'list_price' in vals:
            price  = vals['list_price']
            print("price",price)
            today = fields.Date.today()
            date_before = today - timedelta(days=30)
            print("date before",date_before)
            for rec in self:
                all_orders = self.env['sale.order.line'].search([('product_template_id','=',rec.id),('order_id.state','=','sale'),('order_id.date_order','>',date_before)])
                print("all",all_orders)
                if all_orders:
                    total_price = all_orders.mapped('price_unit')
                    print("price",total_price)
                    average = sum(total_price)/len(total_price)
                    print(average,"avg")
                    if price < average * 0.80:
                        if self.env.user.has_group("sales_team.group_sale_manager"):
                            raise ValidationError("cant be this less price")

            return super().write(vals)

