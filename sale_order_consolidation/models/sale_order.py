# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_merge_quotation(self):
        print("merging quotation", self)
        for rec in self:
            if rec.state !='draft':
                raise ValidationError("Select only draft state!!")
            if len(self) <= 1:
                raise ValidationError("Select more than one orders!!")
            if len(self.mapped('partner_id')) > 1:
                raise ValidationError("choose only one customers order to merge!")


        # len_partner = len(self.mapped('partner_id'))
        # print("partners", len_partner)
        # if len_partner > 1:
        #     raise ValidationError("Can't merge quotation with more than one partner")
        # for rec in self:
        #     if rec.order_line:
        #         for line in rec.order_line:
        #             line=line.ids

        return {
            'type': 'ir.actions.act_window',
            'name': 'Dominating Quotation',
            'res_model': 'assignment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                "default_dominating_ids": self.ids,
            }
        }
