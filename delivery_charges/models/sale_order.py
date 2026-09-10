# -*- coding: utf-8 -*-
from odoo import fields,models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res=super().action_confirm()
        print('fgh')

        product_filter = self.env['product.product'].search(
            [('default_code', '=', 'DCharge'), ('active', '=', True)])

        if not product_filter:
            product_filter = self.env['product.product'].create({
                'name': 'Delivery Charge',
                'default_code': 'DCharge',
                'list_price': 99,
            })

        for rec in self:
            if rec.amount_untaxed < 1500:
                for line in rec.order_line:
                    self.update({
                        'order_line' : [(fields.Command.create({
                            'product_id': product_filter.id,
                            'product_uom_qty': 1,
                            'price_unit':product_filter.list_price,
                            'name' : 'DELIVERY CHARGE',
                        }))]
                    })

        return res