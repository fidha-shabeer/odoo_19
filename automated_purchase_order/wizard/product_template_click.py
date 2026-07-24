# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError


class ProductTemplateClick(models.TransientModel):
    _name = 'product.template.click'
    _description = 'Automated Purchase Order'

    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')

    def action_confirm_btn(self):
        print("Confirm Btn")

        current_id =[(self.env.context['default_product_id'])]
        print("current id: ",current_id)

        temp_id = self.env['product.template'].browse(current_id)
        print("product template id:", temp_id)

        product = temp_id.product_variant_id
        print("product variant id: ", product)

        vendor = temp_id.mapped('seller_ids.partner_id')
        print("vendors list: ", vendor)

        if vendor:
            v = vendor[0]
            print("first vendor: ",v)

        else:
            raise ValidationError("No vendor found")

        draft_rfq = self.env['purchase.order'].search([('partner_id', '=', v.id),
                                                       ('state', '=', 'draft')], limit=1)
        print('existing vendor order: ',draft_rfq)


        if draft_rfq:
            draft_rfq.write({
                'order_line': [fields.Command.create(
                    {
                        'product_id': product.id,
                        'name': product.name,
                        'product_qty': self.quantity,
                        'price_unit': self.price,
                    }
                )]
            })

        if not draft_rfq:
            draft_rfq = self.env['purchase.order'].create({
                'partner_id': v.id,
                'order_line': [fields.Command.create(
                    {
                        'product_id': product.id,
                        'name': product.name,
                        'product_qty': self.quantity,
                        'price_unit': self.price,
                    }
                )]
            })
        # draft_rfq.write({
        #     'state': 'purchase',
        #     })

        draft_rfq.button_confirm()

        print("RFQ ID: ",draft_rfq)

        return {
            'type': 'ir.actions.act_window',
            'name': 'PURCHASE ORDER',
            'res_model': 'purchase.order',
            'res_id': draft_rfq.id,
            'view_mode': 'form',
        }



