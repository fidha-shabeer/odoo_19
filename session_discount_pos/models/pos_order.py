from odoo import fields, models,api

class PosOrder(models.Model):
   _inherit = "pos.order"

   global_discount_amount = fields.Float(string="Global Discount Amount" ,readonly=True,store=True)
   discount_amount = fields.Float(string="Discount Amount" ,readonly=True,store=True)

