# -*- coding: utf-8 -*-
from stdnum.mx import rfc

from odoo import fields, models, api


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "Material Request"
    _rec_name = "state"

    state = fields.Selection(
        selection=[('draft', 'Draft'), ('requested', 'Requested'),
                   ('first_approval', 'First Approval'),
                   ('second_approval', 'Second Approval'),
                   ('rejected', 'Rejected')],
        string="State", default='draft')
    requested_by = fields.Many2one(comodel_name="res.partner",
                                   string="Requested By", required=True)
    requested_date = fields.Datetime(string="Requested Date",
                                     default=fields.Date.today())

    line_ids = fields.One2many(comodel_name="material.information",
                               inverse_name="request_id", string="Lines")

    def button_request(self):
        print("button clicked")
        self.write({"state": "requested"})

    def button_first_approval(self):
        print("button 1 confirm")
        self.write({"state": "first_approval"})

    def button_second_approval(self):
        print("button 2 confirm")
        self.write({"state": "second_approval"})
        for rec in self:
            rfq = self.env['purchase.order'].sudo().create({
                'partner_id': rec.id,
                'order_line': [fields.Command.create(
                    {
                        'product_id': rec.line_ids.product_id.id,
                        'name': rec.line_ids.product_id.name,
                        'product_qty': rec.line_ids.requested_qty,
                    }
                )]
            })
            if rec.line_ids.request_type == 'internal_transfer':
                transfer = self.env['stock.picking'].sudo().create({
                    'partner_id': rec.requested_by.id,
                    'picking_type_id': rec.line_ids.operation_type.id,
                    'location_id': rec.line_ids.source_id.id,
                    'location_dest_id': rec.line_ids.destination_id.id,
                    'move_line_ids': [fields.Command.create({
                        'product_id': rec.line_ids.product_id.id,
                        'quantity_product_uom': 100,
                    })]
                })

            #
            #     rfq = self.env['purchase.order'].sudo().create({
            #     'partner_id': rec.id,
            #     'order_line': [fields.Command.create(
            #         {
            #             'product_id': rec.line_ids.product_id.id,
            #             'name': rec.line_ids.product_id.name,
            #             'product_qty': rec.line_ids.requested_qty,
            #         }
            #     )]
            # })

            # move_id = self.env['account.move'].create({
            #     'move_type': 'out_invoice',
            #     'partner_id': rec.partner_id.id,
            #     'invoice_date': fields.Date.today(),
            # })
            # for l in rec.order_line:
            #     self.env['account.move.line'].create({
            #         'product_id' : l.product_id.id,
            #         'quantity' : l.product_uom_qty,
            #         'price_unit' : l.price_unit,
            #         'move_id' : move_id.id,
            #     })

    def button_reject(self):
        print("button reject")
        self.write({"state": "rejected"})

    # def button_rfq(self):
    #     print("button rfq")
    #
    # def button_transfer(self):
    #     print("button transfer")
