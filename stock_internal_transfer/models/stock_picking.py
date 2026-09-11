# -*- coding: utf-8 -*-
from odoo import models, fields,api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('approve_pending', 'Approve Pending'),('approved', 'Approved')])
    approver_id = fields.Many2one('res.users', string='Approver', required=True )
    is_approver = fields.Boolean(string='Is Approver', compute='_compute_is_approver')
    def action_validate(self):
        print("button validate")
        user= self.env.user
        print(user.name)
        for rec in self:
            approver = rec.approver_id
            print("approver", approver.name)
            if self.env.user.id != approver.id:
                rec.write({'state': 'approve_pending'})
            else:
                rec.write({'state': 'done'})


    def action_confirm(self):
        print("mark as to do")
        for rec in self:
            approver = rec.approver_id
            print("approver", approver.name)
            if self.env.user.id != approver.id:
                rec.write({'state': 'approve_pending'})
            else:
                rec.write({'state': 'done'})
                return super().action_confirm()

    def action_second_approve(self):
        print("approve")
        for rec in self:
            self.write({'state': 'done'})
            # rec.button_validate()


    def _compute_is_approver(self):
        print("is_approver")
        for rec in self:
            if rec.approver_id.id == self.env.user.id:
                print("true")
                rec.is_approver = True
            else:
                print("false")
                rec.is_approver = False

