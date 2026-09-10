from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def action_suggest_alternate(self):
        for move in self.move_raw_ids:
            product = move.product_id

            if product.qty_available <= 0:
                alternates = product.alternate_ids.filtered(
                    lambda p: p.qty_available > 0
                )

                return {
                    "type": "ir.actions.act_window",
                    "name": "Suggest Alternate",
                    "res_model": "alternate.wizard",
                    "view_mode": "form",
                    "target": "new",
                    "context": {
                        "default_component_id": product.id,
                        "default_alternate_ids": [
                            fields.Command.set(alternates.ids)
                        ],
                        "active_id": self.id,
                    },
                }