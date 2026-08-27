from odoo import models, fields

class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   max_discount_limit = fields.Float(string="Session Wise Maximum Discount Limit",
       config_parameter='session_discount_pos.max_discount_limit')
