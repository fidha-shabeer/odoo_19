# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    state = fields.Selection([("draft", "Draft"), ("submitted", "Submitted"),("approved","Approved")])
    note_ids = fields.One2many('product.pricing.notebook','product_id',string="Notes")

