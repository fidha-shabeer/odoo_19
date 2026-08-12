# -*- coding: utf-8 -*-
from odoo import fields,models,api

class PosSession(models.Model):
    _inherit = 'pos.session'

    max_discount_limit = fields.Float(string="Maximum Discount Limit",compute="_compute_max_discount_limit")

    def get_param(self):
        params = self.env['ir.config_parameter'].sudo()
        print("params", params)
        max_discount = params.get_param(
            'session_discount_pos.max_discount_limit')
        print(max_discount,"max_discount xxxxxxxxx")

    def open_frontend_cb(self):
        print("frontend xxxxxxxxx")
        res=super().open_frontend_cb()
        params = self.env['ir.config_parameter'].sudo()
        print("params", params)
        max_discount = params.get_param(
            'session_discount_pos.max_discount_limit')
        print(max_discount, "max_discount xxxxxxxxx")
        return res

    def _compute_max_discount_limit(self):
        print("_compute_max_discount_limit")
        params = self.env['ir.config_parameter'].sudo()
        print("params", params)
        max_discount = params.get_param(
            'session_discount_pos.max_discount_limit')
        print(max_discount, "max_discount xxxxxxxxx")
        for rec in self:
            rec.max_discount_limit = max_discount
            print(rec.max_discount_limit,"max_discount xxxxxxxxx")

    @api.model
    def _load_pos_data_fields(self, config_id):
        """
        Adds the 'max discount limit' field to the list of fields loaded into the POS.
        """
        data = super()._load_pos_data_fields(config_id)
        print("data before", data)
        data += ['max_discount_limit']
        print("data after", data)
        return data

