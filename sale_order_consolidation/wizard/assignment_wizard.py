# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError


class AssignnmentWizard(models.TransientModel):
    _name = 'assignment.wizard'

    dominating_quotation = fields.Many2one('sale.order', string='Dominating quotation')
    dominating_ids = fields.Many2many("sale.order", string="Dominating orders")

    def action_consolidate(self):
        print("consolidate")

        dominating = self.dominating_quotation
        print("dominating", dominating)

        all_selected = self.dominating_ids
        print("all selected", all_selected)

        others = all_selected - dominating
        print("others", others)

        for other in others:
            for recline in dominating.order_line:
                print("line", recline.product_id.display_name)
                for line in other.order_line:
                    if recline.product_id.id == line.product_id.id:
                        recline.product_uom_qty += line.product_uom_qty
                        updated = recline.product_uom_qty
                        print("updated", updated)
                    else:
                        if recline.product_id.id != line.product_id.id:
                            self.dominating_quotation.write({
                                'order_line': [
                                    fields.Command.create({
                                        "product_id": line.product_id.id,
                                        "product_uom_qty": line.product_uom_qty,
                                        "price_unit": line.price_unit,
                                        "name": line.name,
                                    }
                                    )
                                ]
                            })
                            other.write({
                                "state": "cancel"
                            })

                    # self.dominating_quotation.write({
                    #         'order_line': [
                    #             fields.Command.create({
                    #                 "product_id": line.product_id.id,
                    #                 "product_uom_qty": line.product_uom_qty,
                    #                 "price_unit": line.price_unit,
                    #                 "name": line.name,
                    #             }
                    #             )
                    #         ]
                    #     })

                    other.write({
                        "state": "cancel"
                    })



        # quotation = self.dominating_quotation
        # customer = quotation.partner_id
        # print("quotation:", quotation)
        # selected = self.env.context.get("list")
        # records = self.env['sale.order'].browse(selected)
        # print("records:", records)
        # # order = records.search([('partner_id', '=', customer.id)])
        # order = records.filtered(lambda r: r.partner_id.id == customer.id)
        # print("order:", order)
        # for line in order.order_line:
        #     print("line:", line)
        #     print("dsf", self.env['sale.order'].browse(self.dominating_quotation.id))
        #     self.dominating_quotation.write({
        #         'order_line': [
        #             fields.Command.create({
        #                 "product_template_id": line.product_template_id,
        #                 "product_uom_qty": line.product_uom_qty,
        #                 "price_unit": line.price_unit,
        #                 "name": "demo",
        #             }
        #             )
        #         ]
        #     })
        # # self.env['sale.order'].with_context(dominating_quotation=self.dominating_quotation).action_merge_quotation()
        # return True
