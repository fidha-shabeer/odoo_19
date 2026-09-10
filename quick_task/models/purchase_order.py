# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrde(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        for rec in self:
            print("working")
            stage = self.env["project.task.type"].create({
                'name': "In progess"
            })
            for line in rec.order_line:
                projects=rec.order_line.filtered(lambda l :l.product_id.project_id)[:1]

                project = line.product_id.project_id
                print("pro",project)
                first = project.id
                if not first:
                    return super().button_confirm()

                total_qty = sum(rec.order_line.mapped('product_qty'))
                total_price = sum(rec.order_line.mapped('price_unit'))
                print(" qty",total_qty)
                print("price",total_price)

                task = self.env['project.task'].create({
                    'display_name' : f"Purchase Confirmed – {rec.name}",
                    'project_id': project.id,
                    'stage_id':stage.id,
                    'description': f"the total quantities {total_qty}and total value of all products {total_price}.",
                })

                self.env["project.task"].create({
                    "display_name" : line.product_id.name,
                    "parent_id" : task.id,
                    "project_id":project.id,
                })
        return super().button_confirm()








