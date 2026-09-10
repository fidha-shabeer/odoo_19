# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sub_order_ids = fields.One2many(comodel_name="purchase.order",inverse_name="parent_id", relation="purchase_sub_rel", column1="purchas_id", column2="sub_id", string="Sub Orders")
    parent_id = fields.Many2one(comodel_name="purchase.order", default=lambda self:self.id)
    is_sub_order = fields.Boolean(default=False, compute="_compute_is_sub")

    def action_view_order(self):
        print("Vendoe Split Smart Button")
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Split by Lowest Price Vendor',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.sub_order_ids.ids)], }




    def action_split_vendor(self):
        print("split_vendor")

        order_line = self.order_line
        print("order_line:",order_line)

        order = self
        print("order:",order)

        for rec in self:
            for line in rec.order_line:
                vendors = line.product_id.seller_ids
                print("vendors:", vendors)

                price_list = vendors.mapped("price")
                print("price_list:", price_list)

                min_price = min(price_list)
                print("min_price:", min_price)

                for vendor in vendors:
                    if vendor.price == min_price:
                        print("vendor:", vendor.display_name)
                        if vendor:
                            new_po = self.env["purchase.order"].create({
                                'partner_id': vendor.partner_id.id,
                                'parent_id': rec.id,
                                'order_line': [fields.Command.create({
                                    'product_id': line.product_id.id,
                                    'product_qty': line.product_qty,
                                    'price_unit': min_price,
                                })]

                            })

    def _compute_is_sub(self):
        print("compute working")
        for rec in self:
            if rec.sub_order_ids:
                rec.is_sub_order = True
            else:
                rec.is_sub_order = False







