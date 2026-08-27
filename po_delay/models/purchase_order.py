# -*- coding: utf-8 -*-
import datetime

from odoo import fields, models
from datetime import timedelta, datetime


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def po_delay(self):
        print("action started")
        orders = self.search([('state', '=', 'purchase'), ('receipt_status', '=', 'pending')])
        print("orders", orders)
        manager_grp = self.env.ref("purchase.group_purchase_manager")
        print("manager", manager_grp)
        manager = self.env['res.users'].search([('group_ids', '=', manager_grp.id)])
        print("user manager", manager.partner_id.name)

        today = datetime.now()
        print("todayy", today)
        for rec in orders:
            print("rec delivery", rec.date_planned)
            if rec.date_planned < today:
                print("Purchase Order Delay")
                activity = self.env['mail.activity'].search(
                    [('res_model_id', '=', 'res.partner'), ('res_id', '=', rec.partner_id.id)])
                print("activity", activity)

                print("vendor", rec.partner_id.name)
                user = rec.user_id
                print("user", user)

                if not activity:
                    print("no activity till now")
                    activity_type = self.env.ref('mail.mail_activity_data_call')
                    self.env['mail.activity'].create({
                        'activity_type_id': activity_type.id,
                        'res_model_id': self.env['ir.model']._get_id('res.partner'),
                        'res_id': rec.partner_id.id,
                        'user_id': manager.id,
                        'date_deadline': fields.Date.today() + timedelta(days=2),
                        'summary': 'PO delayed...get in touch with the %s'%user.partner_id.name,
                    })

                    rec.message_post(body= "The purchase order %s is delayed.."%rec.name,
                                    subject='po is delayed',
                                    message_type='comment',
                                    subtype_xmlid='mail.mt_comment',
                                    author_id= manager.partner_id.id,
                                    partner_ids = [user.partner_id.id],
                                     )


                # if rec.partner_id.email:
                #     template = self.env.ref("po_delay.po_email_template")
                #     template.send_mail(rec.id, force_send=True)


