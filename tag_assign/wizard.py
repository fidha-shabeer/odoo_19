from odoo import models, fields


class SubstituteWizard(models.TransientModel):
    _name = "substitute.wizard"

    production_id = fields.Many2one("mrp.production")
    component_id = fields.Many2one("product.product")
    alternate_id = fields.Many2one("product.product")

    def action_replace(self):
        move = self.production_id.move_raw_ids.filtered(
            lambda x: x.product_id == self.component_id
        )[:1]

        if move:
            move.product_id = self.alternate_id

        return {"type": "ir.actions.act_window_close"}