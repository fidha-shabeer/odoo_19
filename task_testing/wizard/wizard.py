from odoo import fields, models


class AlternateWizard(models.TransientModel):
    _name = "alternate.wizard"
    _description = "Alternate Component Wizard"

    component_id = fields.Many2one(
        "product.product",
        string="Component",
        readonly=True,
    )

    alternate_ids = fields.Many2many(
        "product.product",
        string="Available Alternates",
        readonly=True,
    )

    alternate_id = fields.Many2one(
        "product.product",
        string="Select Alternate",
    )

    def action_replace(self):
        mo = self.env["mrp.production"].browse(
            self.env.context.get("active_id")
        )

        move = mo.move_raw_ids.filtered(
            lambda x: x.product_id == self.component_id
        )[:1]

        if move:
            move.product_id = self.alternate_id

        return {"type": "ir.actions.act_window_close"}