from odoo import models, fields

class ViewUpdateWizard(models.TransientModel):
    _name = 'view.update.wizard'

    product_ids = fields.Many2many('product.product',string='Product Updated')
    percentage = fields.Float(string='Percentage')
    fixed_price = fields.Float(string='Fixed Price')
    updated_price = fields.Float(string='Updated Price')