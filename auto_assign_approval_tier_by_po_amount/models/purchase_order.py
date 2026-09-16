# -*- coding: utf-8 -*-
from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        print("button conform clicked")
        for rec in self:
            if rec.amount_total < 50000:
                rec.write({
                    "state": "purchase",
                })
            if rec.amount_total >= 50000 and rec.amount_total < 500000:
                if not self.env.user.has_group("purchase.group_purchase_manager"):
                    print("not manager")

                    manager_grp = self.env.ref("purchase.group_purchase_manager")
                    print("manager", manager_grp)
                    manager = self.env['res.users'].search([('group_ids', '=', manager_grp.id)])
                    print("user manager", manager.partner_id.name)


                    rec.write({
                        'state': "to approve",
                    })

                    activity = self.env['mail.activity'].search(
                        [('res_model_id', '=', 'res.partner'), ('res_id', '=', rec.partner_id.id)])
                    print("activity", activity)

            if rec.amount_total > 500000:
                if not self.env.user.has_group("auto_assign_approval_tier_by_po_amount.group_director_purchase"):
                    print("not director")
                    rec.write({
                        'state': "to approve",
                    })



        return super().button_confirm()
