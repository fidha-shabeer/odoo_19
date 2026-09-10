# -*- coding: utf-8 -*-
from odoo import models,fields,api
from odoo.exceptions import ValidationError
print("egyge")
class SaleOrder(models.Model):
    _inherit = "sale.order"


    def action_confirm(self):
        print(213213123)
        return super().action_confirm()

    def action_quotation_send(self):
        print("hyfr",self)
        records = self.env['sale.order'].browse(self)
        if not records.order_lines:
            print(records,"jnrfjrn")
        if not self.order_line:
            raise ValidationError("no sale order exist")
        else:
            return super().action_quotation_sent()
