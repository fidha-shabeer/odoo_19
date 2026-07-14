# -*- coding: utf-8 -*-
# from addons.web.controllers import action
from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('approval_pending', 'Approval Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

    def action_confirm(self):
            param = self.env['ir.config_parameter'].sudo()

            is_discount = param.get_param('discount_approval.is_discount_limit')
            discount_limit = float(param.get_param('discount_approval.discount_limit'))
            print(discount_limit)
            print(is_discount)
            if is_discount:
                for rec in self:
                    for l in rec.order_line:
                        if l.discount > discount_limit:
                            if rec.user_id.has_group('sales_team.group_sale_manager') or rec.user_id.has_group('sales_team.group_sale_salesman_all_leads'):
                                rec.write({'state': 'approval_pending'})
                                return True

            return super().action_confirm()

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})







