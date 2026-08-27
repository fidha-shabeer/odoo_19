# -*- coding: utf-8 -*-
from odoo import fields, models,api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_owner_id = fields.Many2one(comodel_name="res.partner", string="Product Owner")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'product_owner' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        print("data before", data)
        data += ['product_owner_id']
        print("data after", data)
        return data
