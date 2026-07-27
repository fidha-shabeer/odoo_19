from odoo import models, fields
class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   is_required_attachment = fields.Boolean(string="Require Attachment on Purchase Order Confirmation", config_parameter="mandatory_attachment.is_required_attachment")
