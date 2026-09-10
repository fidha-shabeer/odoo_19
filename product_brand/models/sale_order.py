# -*- coding: utf-8 -*-
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_prime_customer = fields.Boolean(string="Is Prime Customer",related="partner_id.is_prime_customer",store=True)

