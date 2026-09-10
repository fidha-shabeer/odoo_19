# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.exceptions import ValidationError


class MrpProductionExt(models.Model):
    _name = 'mrp.production.ext'
    _description = 'Manufacturing Order Task'

    name = fields.Char(default='New')
    product_id = fields.Many2one('product.template',string='Product')
    bom_id = fields.Many2one(string='BOM',comodel_name='mrp.bom')
    quantity = fields.Integer(string='Quantity')
    planned_date = fields.Date(string='Planned Date',default=fields.Date.today())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('cancel', 'Cancelled'),
    ])
    material_line_ids = fields.One2many("mrp.production.material.line","production_id",string='Material Lines')
    required_qty = fields.Float(string='Required Qty')

    @api.model_create_multi
    def create(self, vals_list):
        """Sequence creation """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env["ir.sequence"].next_by_code('productionsequence')
        return super().create(vals_list)

    @api.onchange('bom_id')
    def onchange_bom_id(self):
        self.product_id = self.bom_id.product_tmpl_id
        print(self.product_id)
        self.quantity = self.bom_id.product_qty
        print(self.quantity,"qty")

        for rec in self:
                rec.write({
                'material_line_ids': [fields.Command.create({
                    'production_id': rec.name,
                    'product_id': rec.bom_id.bom_line_ids.product_id.id,
                    'consumed_qty' : rec.bom_id.bom_line_ids.product_qty,
                })]
            })

    @api.onchange('bom_id')
    def _onchange_required_qty(self):
        print("checking",self.material_line_ids.consumed_qty)
        for rec in self:
            if rec.bom_id:
                rec.required_qty = rec.quantity * rec.material_line_ids.consumed_qty
                print("required", self.required_qty)






    # @api.onchange('product_id')
    # def onchange_product_id(self):
    #     if not self.product_id.bom_ids:
    #         print("yes")
    #         raise ValidationError("no bom present")








    # @api.depends('bom_id')
    # def _compute_material_line_ids(self):
    #     for rec in self:
    #         if rec.bom_id:
    #             for l in rec.bom_id:
    #                 rec.material_line_ids.product_id = rec.bom.product_id
    #
    #









