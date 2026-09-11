# -*- coding: utf-8 -*-
from odoo import models, fields

class StockPicking(models.Model):
   _inherit = 'stock.picking'

   invoice_ids = fields.One2many(comodel_name="account.move",inverse_name="transfer_id",string="Invoices")
   reverse_invoice_ids = fields.One2many(comodel_name="account.move", inverse_name="reverse_id", string="Invoices")
