# -*- coding: utf-8 -*-
from odoo import fields, models

class Partner(models.Model):
    _name = "partner.account"
    _description = "Partner Account"

    account_no = fields.Char(string="Account ID")



