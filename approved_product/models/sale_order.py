# -*- coding: utf-8 -*-
from odoo import fields,models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"


