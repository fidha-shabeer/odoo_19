from odoo import models, fields


class BulkPriceUpdate(models.TransientModel):
    _name = 'bulk.price.update.line'

    bulk_id = fields.Many2one(comodel_name="bulk.price.update", string="Bulk Price")
    product_id = fields.Many2one(comodel_name='product.product', string='Products Updated')
    original_price = fields.Float(string='Original Price')
    updated_price = fields.Float(string='Updated Price')

