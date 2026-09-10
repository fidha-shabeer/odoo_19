from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    alternate_product_ids = fields.Many2many(
        "product.product",
        string="Approved Alternate Components"
    )