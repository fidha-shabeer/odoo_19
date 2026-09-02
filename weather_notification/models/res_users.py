# -*- coding: utf-8 -*-
from odoo import fields, models
class ResUsers(models.Model):
    _inherit = "res.users"

    type = fields.Selection([
        ("coordinates", "Coordinates"), ("location", "Location")
    ],default="location")
    longitude = fields.Float(string="Longitude")
    latitude = fields.Float(string="Latitude")
    location = fields.Char(string="Location")























