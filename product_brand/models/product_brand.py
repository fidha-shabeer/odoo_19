# -*- coding: utf-8 -*-
from odoo import fields, models,api

class ProductBrand(models.Model):
    _name = "product.brand"
    _description = "Product Brand"
    _rec_name = "product_brand"

    product_brand = fields.Char(string="Brand Name" ,required=True)
