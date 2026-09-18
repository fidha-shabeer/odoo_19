# -*- coding: utf-8 -*-
from odoo import fields, models, api

class MailActivity(models.Model):
    _inherit = "mail.activity"

    unique_name = fields.Char(string="Unique Name")