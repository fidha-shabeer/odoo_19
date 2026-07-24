# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # invoice_id = fields.Many2one(comodel_name='account.move', string="Invoice")
    # invoice = fields.Char(string="Invoice")

    def action_pay(self):
        print("can pay soon workin on it.....")

        for rec in self:
            move_id = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec.partner_id.id,
                'invoice_date': fields.Date.today(),
            })
                # 'invoice_line_ids': [(fields.Command.create({
                #     'product_id': rec.order_line.product_id.id,
                #     'quantity': rec.order_line.product_uom_qty,
                #     'price_unit': rec.order_line.price_unit,
                # }))], })
            for l in rec.order_line:
                self.env['account.move.line'].create({
                    'product_id' : l.product_id.id,
                    'quantity' : l.product_uom_qty,
                    'price_unit' : l.price_unit,
                    'move_id' : move_id.id,
                })
            # rec.invoice_ids = move_id.id
            # print("recccc",rec.invoice_ids)
            print("partner", rec.partner_id.id)
            print("product", l.product_id.id)
            print('quantity', l.product_uom_qty)
            print('price_unit',l.price_unit, )

            move_id.action_post()

            # pay_rec = self.env["account.payment.register"].create({
            #
            # })
            rec.action_confirm()

    def action_view_invoice(self):
        print("printing invoice smart button.....")
        #
        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'account.move',
        #     'res_id': self.invoice_ids.id,
        #     'view_mode': 'form',
        #
        # }
