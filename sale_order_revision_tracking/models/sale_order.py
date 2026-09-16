# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    revision_ids = fields.One2many(comodel_name='sale.order.revision',inverse_name='sale_id',string='Revisions')
    revision_count = fields.Integer(string='Number of Revisions', compute='_compute_count')


    @api.depends('revision_ids')
    def _compute_count(self):
        for rec in self:
            if rec.revision_ids:
                rec.revision_count = len(rec.revision_ids)
        print(rec.revision_count)

    def action_sale_revision(self):
        print("action_sale_revision")
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sale Order Revision',
                'res_model': 'sale.order.revision',
                'view_mode': 'list',
                'domain': [('sale_id', '=', rec.id)],
            }

    def write(self, vals):
        print("write",vals)
        print("self",self)
        for rec in self:
            note = " "
            if rec.state == 'sent':
                print("yes")

                if 'state' in vals:
                    state = vals['state']
                    print(state,"state")
                    note += f"the state is updated from {rec.state} to {state}\n"
                    print("note",note)

                if 'order_line' in vals:
                    print("order_line",rec.order_line)
                    for line in vals['order_line']:
                        print("line",line)
                        if line[0] == 0:
                            note+="new line created!! \n"
                            print(line[1],"id")
                            print(line[2], "values")
                            if 'product_id' in line[2]:
                                product = self.env['product.product'].browse(line[2].get('product_id'))
                                note += f"Product : {product.name} \n"
                            if 'product_uom_qty' in line[2]:
                                qty = line[2].get('product_uom_qty')
                                note += f"Quantity : {qty} \n"

                        if line[0] == 1:
                            rec_id = line[1]
                            print("Rec ID", rec_id)
                            note += f"sale order line {rec_id} edited.... \n"

                            if 'product_id' in line[2]:
                                product = self.env['product.product'].browse(line[2].get('product_id'))
                                note += f"Product : {product.name} \n"

                            if 'product_uom_qty' in line[2]:
                                qty = line[2].get('product_uom_qty')
                                note += f"Quantity : {qty} \n"

                            if 'price_unit' in line[2]:
                                price = line[2].get('price_unit')
                                print(price,"price")
                                note+= f"Price : {price} \n"

                        if line[0] == 2:
                            rec_id = line[1]
                            print("Rec ID", rec_id)
                            note += f"sale order line {rec_id} deleted.."

                    self.env['sale.order.revision'].create({
                        'sale_id' : self.id,
                        'revision_number' : len(rec.revision_ids)+1,
                        'modified_by': self.env.user.id,
                        'modified_on': fields.Datetime.now(),
                        'change_notes': note,

                    })
        return super().write(vals)


