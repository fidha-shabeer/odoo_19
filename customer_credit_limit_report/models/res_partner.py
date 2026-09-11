# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit = fields.Float(string="Total Receivable",compute = "_compute_credit")
    sales_outstanding = fields.Float(string="Days Sales Outstanding(DSO)")
    partner_limit = fields.Float(string="Partner Limit")

    @api.depends("sales_outstanding")
    def _compute_credit(self):
        print("computing credit")
        for record in self:
            print("record:",record.credit)


