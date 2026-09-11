# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    project_id = fields.Many2one("project.project",string="project")
    last_price_update = fields.Date(string="last update")