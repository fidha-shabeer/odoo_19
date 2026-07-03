from odoo import models, fields


class AccountMove(models.Model):
   _inherit = 'account.move'

   billing = fields.Many2one('billing.schedule',string='Subscription')