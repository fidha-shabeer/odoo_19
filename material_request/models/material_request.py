# -*- coding: utf-8 -*-
from odoo import fields, models

class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "Material Request"
    _rec_name = "state"
    _inherit = ['mail.thread']

    state = fields.Selection(
        selection=[('draft', 'Draft'), ('requested', 'Requested'),
                   ('first_approval', 'First Approval'),
                   ('second_approval', 'Second Approval'),
                   ('rejected', 'Rejected')],
        string="State", default='draft', tracking=True)
    requested_by = fields.Many2one(comodel_name="res.users",
                                   string="Requested By", store=True,
                                   default=lambda self: self.env.user.id)
    requested_date = fields.Datetime(string="Requested Date",
                                     default=fields.Date.today())

    line_ids = fields.One2many(comodel_name="material.information",
                               inverse_name="request_id", string="Lines")

    def button_request(self):
        '''request button'''
        print("button clicked")
        self.write({"state": "requested"})

    def button_first_approval(self):
        '''first approval button'''
        print("button 1 confirm")
        self.write({"state": "first_approval"})

    def button_second_approval(self):
        '''second approval button and the creation of rfq and internal transfer take place here'''
        print("button 2 confirm")
        self.write({"state": "second_approval"})
        trans = self.env['stock.picking.type'].search(
            [('code', '=', 'internal')])
        print("transfer", trans)
        print(trans.code)
        for rec in self:
            for l in rec.line_ids:
                if l.request_type == 'purchase_order':
                    for v in l.vendor_id:
                        rfq = self.env['purchase.order'].sudo().create({
                            'partner_id': v.id,
                            'order_line': [fields.Command.create(
                                {
                                    'product_id': l.product_id.id,
                                    'name': l.product_id.name,
                                    'product_qty': l.requested_qty,
                                }
                            )]
                        })
                if l.request_type == 'internal_transfer':
                    transfer = self.env['stock.picking'].sudo().create({
                        'partner_id': rec.requested_by.id,
                        'picking_type_id': trans.id,
                        'location_id': l.source_id.id,
                        'location_dest_id': l.destination_id.id,
                        'move_ids': [fields.Command.create({
                            'product_id': l.product_id.id,
                            'product_uom_qty': l.requested_qty,
                        })]
                    })

    def button_reject(self):
        print("button reject")
        self.write({"state": "rejected"})

    # def button_rfq(self):
    #     print("button rfq")
    #
    # def button_transfer(self):
    #     print("button transfer")
