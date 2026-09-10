# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    restrict_ids = fields.Many2many(comodel_name="product.template", relation='product_restrict_rel',
                                    column1='product_id',
                                    column2='restrict_product_id',
                                    string='restrict_product')
