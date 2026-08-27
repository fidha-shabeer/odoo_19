# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for rec in self:
            res = super().action_confirm()
            print("action_confirm clicked")

            stage = rec.team_id.crm_state_id.name
            print("stage",stage)

            lead_stage=rec.opportunity_id.stage_id.name
            print("lead_stage",lead_stage)

            if rec.opportunity_id.stage_id.id != rec.team_id.crm_state_id.id:
                rec.opportunity_id.stage_id = rec.team_id.crm_state_id.id
            print("rec.opportunity_id.stage_id.id",rec.opportunity_id.stage_id.id)

        return res
