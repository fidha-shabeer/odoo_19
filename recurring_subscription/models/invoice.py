from odoo import models, fields


class AccountMove(models.Model):
   _inherit = 'account.move'

   subscription_id = fields.Many2one('billing.subscription',string='Subscription')