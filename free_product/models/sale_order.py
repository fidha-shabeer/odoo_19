# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    exclude_product_ids = fields.Many2many('product.product',
                                           string="Exclude Products")

    def action_free(self):
        print("freee")
        product = self.env["product.product"].search(
            [('is_free_product', '=', True)])
        print("product search", product)
        # free_pro = product.filtered(lambda l: l.is_free_product)
        if not product:
            raise ValidationError("Free product not available")
        print("products", product)
        if self.exclude_product_ids:
            print("exclude product ids", self.exclude_product_ids)

        # print("free_pro", free_pro)
        for rec in self:
            if product:
                for fpro in product:
                    if fpro not in rec.order_line.product_id:
                        if fpro not in rec.exclude_product_ids:
                            rec.write({
                                'order_line': [(fields.Command.create({
                                    'product_id': fpro.id,
                                    'product_uom_qty': 1,
                                    'price_unit': 0.0,
                                    'name': fpro.name,
                                }))]
                            })

        # for rec in self:
        #     for fpro in free_pro:
        #         line = self.env['sale.order.line'].create({
        #             'product_template_id':fpro.name,
        #             'product_uom_qty': 1,
        #             'price_unit': fpro.list_price,
        #             'name': fpro.name,
        #             'order_id': rec.id,
        #         })

        # for line in rec.order_line:
        #     for fpro in free_pro:
        #         rec.write({
        #             'order_line': [(fields.Command.create([{
        #                 'product_id': f.id,
        #                 'product_uom_qty': 0,
        #                 'price_unit': f.list_price,
        #                 'name': 'Free Product',
        #             }]))]
        #         })
