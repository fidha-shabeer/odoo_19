# -*- coding: utf-8 -*-
from openpyxl.worksheet import related

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_free = fields.Boolean(default=False, string="Is Free",
                             related="product_id.is_free_product")

    def action_exclude(self):
        print("exclude button clicked")
        for rec in self:
            print(rec)
            for r in rec.product_id:
                rec.order_id.write({
                    'exclude_product_ids': [fields.Command.link(r.id)]
               })
            rec.unlink()
