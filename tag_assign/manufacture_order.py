from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def action_suggest_alternate(self):

        component = self.move_raw_ids.filtered(
            lambda x: x.product_id.qty_available <= 0
        )[:1]

        return {
            "type": "ir.actions.act_window",
            "name": "Suggest Alternate",
            "res_model": "substitute.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_production_id": self.id,
                "default_component_id": component.product_id.id,
            },
        }