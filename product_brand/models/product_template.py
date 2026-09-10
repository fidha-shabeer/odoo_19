# -*- coding: utf-8 -*-
from odoo import fields,models,_
from zeep.xsd.types.builtins import default_types

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_brand = fields.Many2one(comodel_name="product.brand",string="Product Brand")
    product_master_type = fields.Selection(selection =[('single_product', 'Single Product'), ('branded_product', 'Branded Product')],default='single_product',required=True)
