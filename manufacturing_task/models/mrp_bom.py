# -*- coding: utf-8 -*-
from odoo import fields, models,api

class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.onchange('product_id')
    def _onchange_product_id(self):
        print(self)
        for rec in  self:
            for line in rec.product_id:
                print(line.product_id)
