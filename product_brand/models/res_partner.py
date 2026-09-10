# -*- coding: utf-8 -*-
from odoo import fields, models,api

class ResPartner(models.Model):
    _inherit = "res.partner"

    is_prime_customer = fields.Boolean(string="Is Prime Customer")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        print("whether workinggggg")
        if self.partner_id:
            self.is_prime_customer = self.partner_id.is_prime_customer
        else:
            self.is_prime_customer = ""



        # for rec in self:
        #     if rec.partner_id.is_prime_customer:
        #         rec.is_prime_customer = rec.partner_id.is_prime_customer

