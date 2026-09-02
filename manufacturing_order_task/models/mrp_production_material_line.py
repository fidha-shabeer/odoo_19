# -*- coding: utf-8 -*-
from odoo import fields, models,api

class MrpProductionMaterialLine(models.Model):
    _name = 'mrp.production.material.line'
    _description = 'Material Line'

    production_id = fields.Many2one('mrp.production.ext',string='Production')
    product_id = fields.Many2one('product.product',string='Product')
    required_qty = fields.Integer(string = 'Required Qty')
    available_qty = fields.Integer(string = 'Available Qty',compute='_compute_available_qty',store=True)
    consumed_qty =fields.Integer(string = 'Consumed Qty')
    is_material_available = fields.Boolean(string='Is Material Available')

    @api.depends('product_id.qty_available','product_id')
    def _compute_available_qty(self):
        print(self.product_id.qty_available,"qty")
        print("compute_available_qty")
        for rec in self:
            if rec.product_id:
                rec.available_qty = rec.product_id.qty_available
                print("available",rec.available_qty)

    @api.onchange('consumed_qty','available_qty')
    def onchange_required_qty(self):
        self.required_qty = self.available_qty * self.consumed_qty
        print("required",self.required_qty)








