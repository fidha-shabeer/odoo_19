# -*- coding: utf-8 -*-
import datetime

from odoo import fields, models
from datetime import timedelta,datetime


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        print("showww")
        for rec in self:
            rec.po_delay()
        super().button_confirm()

    def po_delay(self):
        print("action started")
        po = self.search([('date_planned', '<', datetime.now()), ('state', '=', 'purchase')])
        print(po)
        today = datetime.now()
        print(today)
        print(self.date_planned,"planned")
        for rec in self:
            if rec.state == 'purchase' and rec.date_planned < today:
                print("Purchase Order Delay")
                template = self.env.ref("po_delay.po_email_template")
                email_values = {'email_from': self.env.user.email}
                template.send_mail(rec.id, force_send=True, email_values=email_values)

                self.message_post(body=_("Dear vendor, PO has been delayed."),
                                  subject='Delay',
                                  message_type='email',
                                  subtype_xmlid='mail.mt_comment',
                                  )

    # date_filter = fields.Datetime.now() - timedelta(days=90)
    # print("date:", date_filter)
    # products = self.env["product.product"].search([('active', '=', True)])
    # print("active products", products)
    #
    # for pro in products:
    #     sold_filter = self.env['sale.report'].search([('product_id', '=', pro.id), ('state', '=', 'sale')],
    #                                                  order='date desc', limit=1)
    #     print("filtered sale", sold_filter)
    #     if not sold_filter:
    #         pro.write({'active': False})
    #     elif sold_filter.date < date_filter:
    #         pro.write({'active': False})
