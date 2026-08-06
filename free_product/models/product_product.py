# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"

    is_free_product = fields.Boolean(string="Is Free Product")