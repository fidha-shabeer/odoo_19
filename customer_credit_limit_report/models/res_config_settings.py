from odoo import models, fields
class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   is_sales_credit = fields.Boolean(string="Sales Credit", config_parameter='customer_credit_limit_report.is_sales_credit')
   credit_limit = fields.Float(string="Credit Limit", config_parameter='customer_credit_limit_report.credit_limit')
