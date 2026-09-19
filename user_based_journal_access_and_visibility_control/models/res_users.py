# -*- coding: utf-8 -*-
from odoo import fields, models
class ResUsers(models.Model):
    _inherit = "res.users"

    journal_ids = fields.Many2many(comodel_name='account.journal')


