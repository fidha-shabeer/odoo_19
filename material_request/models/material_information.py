# -*- coding: utf-8 -*-
from odoo import fields, models,api

class MaterialInformation(models.Model):
    _name = "material.information"
    _description = "Material Information"

    request_id = fields.Many2one(comodel_name="material.request",string="Request ID")
    product_id = fields.Many2one("product.product", string="Product",required=True)
    requested_qty = fields.Integer(string="Requested Qty")
    request_type = fields.Selection(selection=[("purchase_order","Purchase Order"),('internal_transfer','Internal Transfer')],string="Request Type",default="purchase_order")
    vendor_id = fields.Many2many("res.partner", string="Vendors")
    source_id = fields.Many2one(comodel_name="stock.location", string="Source Location")
    destination_id = fields.Many2one(comodel_name="stock.location", string="Destination Location")
    operation_type = fields.Many2one(comodel_name="stock.picking.type",string="Operation Type")