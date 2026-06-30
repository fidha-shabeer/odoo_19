from odoo import models, fields


class AccountMove(models.Model):
   _inherit = 'account.move'

   subscription_ids = fields.Char(string='Subscriptions')