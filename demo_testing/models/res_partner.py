# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    product_allowed_ids = fields.Many2many('product.template',string="allowed product")

