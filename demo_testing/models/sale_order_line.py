# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    allowed_product = fields.Many2many('product.template',related= "order_id.partner_id.product_allowed_ids",string="allowed products")