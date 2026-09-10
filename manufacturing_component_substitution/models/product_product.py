# -*- coding: utf-8 -*-

from odoo import fields,models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    alternate_product_id = fields.Many2many(comodel_name="product.product", relation="product_alternate_rel", column1="product_id", column2="alternate_id", string="Alternate Product")
