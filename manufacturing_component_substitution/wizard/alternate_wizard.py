# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError


class AlternateWizard(models.TransientModel):
    _name = 'alternate.wizard'

    mo_id = fields.Many2one('mrp.production',string='Manufacture Order')
    component_id = fields.Many2one("product.product",string="Component")
    alternate_ids = fields.Many2many("product.product",string="Alternate Products domain ")
    alternate_product_id = fields.Many2one("product.product",string="Alternate Product")


    def action_replace(self):
        print("replacing alternate product")

        order = self.mo_id
        print("order: ", order)

        for line in order.move_raw_ids:
            if line.product_id.qty_available<=0:
                print("True")
                line.product_id = self.alternate_product_id.id
                print("replaced: ", line.product_id)



