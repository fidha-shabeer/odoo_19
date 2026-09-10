# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    is_alternate_required = fields.Boolean(default=False, compute="_compute_is_alternate_required", store=True)

    def action_alternate(self):
        print("suggesting alternate product")
        for rec in self:
            for line in rec.move_raw_ids:
                if line.product_id.qty_available <= 0:
                    component = line.product_id
                    print("component",component.display_name)

                    alternates = line.product_id.alternate_product_id.ids
                    print("alternate",alternates)

                    order = self.id
                    print("order",order)



        self.ensure_one
        return {
            'type': 'ir.actions.act_window',
            'name': 'Suggest Alternate Product',
            'res_model': 'alternate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                "default_component_id": component.id,
                "default_alternate_ids": alternates,
                "default_mo_id": order,
            }
        }

    @api.depends("move_raw_ids.product_id")
    def _compute_is_alternate_required(self):
        for rec in self:
            if rec.move_raw_ids.product_id:
                for line in rec.move_raw_ids:
                    if line.product_id.qty_available <= 0:
                        rec.is_alternate_required = True
                    else:
                        rec.is_alternate_required = False
