# -*- coding: utf-8 -*-
from odoo import models,fields,api
class ProductTemplate(models.Model):
    _inherit = "product.template"

    avg_cost = fields.Float(string="Average Purchase Cost", compute="_compute_avg_cost")

    # @api.depends('purchase_order.product_qty','purchase_order.price_unit')
    def _compute_avg_cost(self):
        """ Compute the average cost of the product """
        for rec in self:
            total_qty = 0
            lines = self.env['purchase.order.line'].search([('product_id','=',rec.id),('state','=','purchase')])
            total_qty = sum(lines.mapped('product_qty'))
            total_amount = sum(l.product_qty * l.price_unit for l in lines)

            if total_qty > 0:
                rec.avg_cost = total_amount / total_qty
            else:
                rec.avg_cost = 0

            print(total_amount,total_qty,rec.avg_cost)



