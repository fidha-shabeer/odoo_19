# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    product_combination = fields.Many2one(comodel_name="product.template",string="Product Combination")