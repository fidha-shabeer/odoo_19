# -*- coding: utf-8 -*-
from odoo import fields,models,_
class ProductTemplate(models.Model):
    _inherit = "product.template"

    purchase = fields.Char(string="Purchase Order")
    # purchase_id = fields.Many2one('purchase.order.line',string="Purchase Order")
    def action_click(self):
        print("hello clicked!!!")

        return {
            'type': 'ir.actions.act_window',
            'name': 'PURCHASE ORDER',
            'res_model': 'product.template.click',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_id': self.id,
            }
        }

    def action_auto_purchase(self):
        print("will print soon")
        pro_id = self.env['purchase.order'].search([('order_line.product_id.product_tmpl_id','=',self.id)],order="id desc",limit=1)
        print("fetch_id",pro_id.id)
        fetch = pro_id.id

        return {
            'type': 'ir.actions.act_window',
            'name': 'PURCHASE ORDER',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'target': 'current',
            'domain' : [('id','=',fetch)],
        }
