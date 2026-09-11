# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_update_date(self):
        print(self)
        if len(self) <= 1:
            raise ValidationError("Should contain more than one sale order 1 order!!")

        for rec in self:
            if rec.state != 'draft' and rec.state != 'sent':
                raise ValidationError("Select only orders in draft and sent states!!")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Expected Delivery Date',
            'res_model': 'expected.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_quotation_ids': self.ids,
            }
        }