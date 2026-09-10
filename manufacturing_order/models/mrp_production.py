# -*- coding: utf-8 -*-

from odoo import fields,models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    partner_id = fields.Many2one('res.partner',string="customer")
