# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductTemplateClick(models.TransientModel):
    _name = 'product.template.click'
    _description = 'Automated Purchase Order'

    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')


    def action_confirm_btn(self):
        print("Confirm Btn")
       
        testing  = self.env['product.template'].browse([(self._context['default_product_id'])])
        print("kkmrk", testing)
        vendor = testing.mapped('seller_ids.partner_id')
        print("vend1", vendor)
        if vendor:
            v = vendor[0]
        print(v)

        rfq = self.env['purchase.order'].create({
            'partner_id' : v.id,
            'order_line' : [fields.Command.create(
                {
                    'product_id' : testing.id ,
                    'name': "DISPLY",
                    'product_qty' : self.quantity,
                    'price_unit' : self.price,
                }
            )]
        })





