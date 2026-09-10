from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    alternative_ids = fields.Many2many(
        comodel_name="product.product",
        relation="product_alternative_rel",
        column1="prodct_id",
        column2="alternate_product_id",
        string="alternative Products",
    )