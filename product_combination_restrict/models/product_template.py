from odoo import fields,models,_

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_combination = fields.Many2one(comodel_name="product.template",string="Product Combination")