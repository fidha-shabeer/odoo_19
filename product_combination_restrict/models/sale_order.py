# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        print("clicking")

        for rec in self:
            pro_comb=self.env['product.product'].search([]).filtered(lambda l:l.product_combination)
            print(pro_comb,"combinations")
            pros = pro_comb.mapped('product_combination')
            for pro in pros:
                print("dis",pro.display_name)
            for line in rec.order_line:
                if line.product_id.product_combination in line.product_id:
                    if not line.product_id.product_combination:
                        raise ValidationError("should not contain combination")
            return super().action_confirm()




