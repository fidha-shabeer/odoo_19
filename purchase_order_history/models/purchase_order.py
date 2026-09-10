# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    po_history = fields.Char(string="Purchase Order History")

    def write(self, vals):
        print("sdfghjkl",vals)

    def action_history(self):
        print("history loading...")

        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Purchase Order History',
                'res_model': 'po.tracker',
                'view_mode': 'list,form',
                'domain': [('id', 'in', rec.id)], }
