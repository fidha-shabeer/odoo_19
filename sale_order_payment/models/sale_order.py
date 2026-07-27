# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_pay(self):
        print("can pay soon workin on it.....")

        for rec in self:
            rec.action_confirm()

            policy = rec.order_line.product_template_id.invoice_policy
            print("policy", policy)

            invoices = rec._create_invoices()
            if invoices.state == 'draft':
                    invoices.action_post()

            payment = self.env['account.payment.register'].with_context(active_model = 'account.move', active_ids = invoices.ids).create({
                'amount' : invoices.amount_total,
            })
            for p in payment:
                p.action_create_payments()



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
            #
            # move_id.action_post()

        # ------------
        #         'invoice_line_ids': [(fields.Command.create({
        #             'product_id': rec.order_line.product_id.id,
        #             'quantity': rec.order_line.product_uom_qty,
        #             'price_unit': rec.order_line.price_unit,
        #         }))], }

            # payment = self.env['account.payment.register'].with_context(active_model = 'account.move', active_ids = invoice.ids).create({
            #     'amount' : invoice.amount_total,
            # })
            # for p in payment:
            #     p.action_create_payments()


            # print("partner", rec.partner_id.id)
            # print("product", l.product_id.id)
            # print('quantity', l.product_uom_qty)
            # print('price_unit',l.price_unit, )
            # print( 'amount', move_id.amount_total)


