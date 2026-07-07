# -*- coding: utf-8 -*-
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "sale.order"

    discount = fields.Float(string="Vip Discount", compute="_compute_discount",store=True)

    def _compute_discount(self):
        for rec in self:
            vip_dis = self.env['res.partner'].search([('is_vip', '=', True)])
            for vip in vip_dis:
                if vip_dis:
                    self.discount = vip.vip_discount
            else:
                self.discount = 0

