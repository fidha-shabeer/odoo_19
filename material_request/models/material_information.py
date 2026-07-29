# -*- coding: utf-8 -*-
from odoo import fields, models,api

class MaterialInformation(models.Model):
    _name = "material.information"
    _description = "Material Information"
    _inherit = ['mail.thread']

    request_id = fields.Many2one(comodel_name="material.request",string="Request ID")
    product_id = fields.Many2one("product.product", string="Product",required=True,tracking=True)
    requested_qty = fields.Integer(string="Requested Qty",required=True)
    request_type = fields.Selection(selection=[("purchase_order","Purchase Order"),('internal_transfer','Internal Transfer')],string="Request Type",default="purchase_order",tracking=True)
    vendor_id = fields.Many2many("res.partner", string="Vendors",required=True,tracking=True)
    source_id = fields.Many2one(comodel_name="stock.location", string="Source Location",required=True,tracking=True)
    destination_id = fields.Many2one(comodel_name="stock.location", string="Destination Location",required=True,tracking=True)
    # operation_type = fields.Many2one(comodel_name="stock.picking.type",string="Operation Type")