# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError


class ExpectedDateWizard(models.TransientModel):
    _name = 'expected.date.wizard'

    new_delivery_date = fields.Date('New Delivery Date',default=fields.Date.today)
    reason = fields.Text(string='Reason')

    def action_update(self):
        print("soon updating")
        record_id = self.env.context.get('default_quotation_ids')
        print(record_id,"record_id")
        sale_order = self.env['sale.order'].browse(record_id)
        print(sale_order,"sale order")
        len_sale = len(sale_order)
        print(len_sale,"len_sale")
        for rec in sale_order:
            print("rec",rec)
            rec.commitment_date = self.new_delivery_date
            print("updated",rec.commitment_date)
            rec.message_post(body=f"Reason {self.reason}" ,
                         subject='The reason to update',
                         message_type='comment',
                         subtype_xmlid='mail.mt_comment',
                         )

            # return {
            #     'type': 'ir.actions.client',
            #     'tag': 'display_notification',
            #     'params': {
            #         'type': 'Successfully Updated the Delivery Date',
            #         'message': f'Successfully Updated the Delivery Date of {len_sale} quotations', }
            #
            # }
        return True



