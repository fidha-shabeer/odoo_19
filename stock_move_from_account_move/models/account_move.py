# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountMove(models.Model):
   _inherit = 'account.move'

   source_id = fields.Many2one(comodel_name="stock.location", string="Source Location", required=True, ondelete="cascade")
   destination_id = fields.Many2one(comodel_name="stock.location", string="Destination Location", required=True, ondelete="cascade")
   transfer_id = fields.Many2one(comodel_name="stock.picking",string="Transfer")
   reverse_id = fields.Many2one(comodel_name="stock.picking",string="Reverse")
   is_transfer = fields.Boolean(string="Is Transfer", compute = "_compute_is_transfer" )
   is_reverse = fields.Boolean(string="Is Reverse", compute = "_compute_is_reverse" )

   def action_post(self):
       res = super().action_post()
       for rec in self:
           source = rec.source_id
           print("source", source)
           destination = rec.destination_id
           print("destination", destination)

           pick_type = self.env['stock.picking.type'].search([('code','=','internal')])
           print("pick_type", pick_type.name)
           for line in rec.invoice_line_ids:
               print("line product",line.product_id.id,"qty",line.quantity)
               transfer = self.env['stock.picking'].create({
                   'partner_id': rec.partner_id.id,
                   'picking_type_id': pick_type.id,
                   'location_id': source.id,
                   'location_dest_id': destination.id,
                   'move_type' : 'direct',
                   'move_ids': [fields.Command.create({
                       'product_id': line.product_id.id,
                       'product_uom_qty': line.quantity,
                   })]
               })
               rec.transfer_id = transfer.id
               print("transfer_id", transfer.id)

               # return {
               #     'type': 'ir.actions.act_window',
               #     'res_model': 'stock.picking',
               #     'view_mode': 'list,form',
               #     'domain': [('id', '=', transfer.id)],
               # }

       return res

   def action_reverse(self):
       print("action_reverse")
       res = super().action_reverse()
       for rec in self:
           source = rec.destination_id
           print("source", source)
           destination = rec.source_id
           print("destination", destination)

           pick_type = self.env['stock.picking.type'].search([('code', '=', 'internal')])
           print("pick_type", pick_type.name)
           for line in rec.invoice_line_ids:
               print("line product", line.product_id.id, "qty", line.quantity)
               transfer = self.env['stock.picking'].create({
                   'partner_id': rec.partner_id.id,
                   'picking_type_id': pick_type.id,
                   'location_id': source.id,
                   'location_dest_id': destination.id,
                   'move_type': 'direct',
                   'move_ids': [fields.Command.create({
                       'product_id': line.product_id.id,
                       'product_uom_qty': line.quantity,
                   })]
               })
               rec.reverse_id = transfer.id

       return res

   def action_transfer(self):
       print("action_transfer")
       return {
           'type': 'ir.actions.act_window',
           'res_model': 'stock.picking',
           'view_mode': 'list,form',
           'domain': [('id', '=', self.transfer_id.id)],
       }

   def action_reverse_transfer(self):
       print("action_reverse_transfer")
       return {
           'type': 'ir.actions.act_window',
           'res_model': 'stock.picking',
           'view_mode': 'list,form',
           'domain': [('id', '=', self.reverse_id.id)],
       }

   def _compute_is_transfer(self):
       print("_compute_is_transfer")
       for rec in self:
           if rec.transfer_id:
               rec.is_transfer = True
           else:
               rec.is_transfer = False

   def _compute_is_reverse(self):
       print("_compute_is_reverse")
       for rec in self:
           if rec.reverse_id:
               rec.is_reverse = True
           else:
               rec.is_reverse = False



