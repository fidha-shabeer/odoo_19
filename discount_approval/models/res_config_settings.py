from odoo import models, fields
class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   is_discount_limit = fields.Boolean(string="Discount Limit", config_parameter='discount_approval.is_discount_limit')
   discount_limit = fields.Float(string="Discount Limit%", config_parameter='discount_approval.discount_limit')
