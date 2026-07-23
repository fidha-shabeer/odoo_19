# -*- coding: utf-8 -*-
from odoo import models,_
class ProductTemplate(models.Model):
    _inherit = "product.template"

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
