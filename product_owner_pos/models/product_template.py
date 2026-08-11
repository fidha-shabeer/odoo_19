# -*- coding: utf-8 -*-
from odoo import fields, models,api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_owner_id = fields.Many2one(comodel_name="res.partner", string="Product Owner")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'age' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        print("data before", data)
        data += ['product_owner_id']
        print("data after", data)
        return data


    # def _loader_params_product_product(self):
    #     print("zxcvbnm,.")
    #     result = super()._loader_params_product_product()
    #     print("result bfr", result)
    #     result["search_params"]["fields"].append("product_owner_id")
    #     # print("result aftr", result)
    #     return result