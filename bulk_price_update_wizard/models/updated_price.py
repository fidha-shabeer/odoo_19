from odoo import models, fields

class UpdatedPrice(models.Model):
    _name = 'updated.price'

    product_id = fields.Many2one(comodel_name='product.product',string='Products Updated')
    original_price = fields.Float(string='Original Price')
    updated_price = fields.Float(string='Updated Price')




