# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductPricingNotebook(models.Model):
    _name = 'product.pricing.notebook'

    product_id = fields.Many2one("product.product",string="Product")
    min_qty =fields.Integer(string="Minimum Quantity")
    unit_price = fields.Float(string="Price")
    partner_id = fields.Many2one("res.partner",string="Customer")
