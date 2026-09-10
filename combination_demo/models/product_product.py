from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_combination = fields.Many2many(
        comodel_name="product.product",
        relation="product_combination_rel",
        column1="product_id",
        column2="combination_product_id",
        string="Combination Products",
    )