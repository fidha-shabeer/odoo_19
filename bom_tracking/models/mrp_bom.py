# -*- coding: utf-8 -*-
from odoo import fields, models,api


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    bom_count = fields.Integer(string="BOM History",compute='_compute_bom_count')
    track_ids =fields.One2many(comodel_name='bom.tracker',inverse_name='bom_id',string='Tracker')

    def action_history(self):
        print("history loading...")
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'BOM History',
                'res_model': 'bom.tracker',
                'view_mode': 'list,form',
                'domain': [('bom_id', '=', rec.id)],
            }

    @api.depends('track_ids')
    def _compute_bom_count(self):
        '''compute revision count'''
        for rec in self:
            rec.bom_count = len(rec.track_ids)

    def write(self, vals):
        for rec in self:
            print("vals_list", vals)

            note = ''
            if 'product_qty' in vals:
                print("Testing..")
                qty = str(vals['product_qty'])
                note += "The quantity changed to : %s" %qty +"\n"

            if 'product_tmpl_id' in vals:
                product = self.env['product.template'].browse(vals['product_tmpl_id'])
                print("product",product)
                note += f"The Product changed to : {product.display_name} \n"

            if 'product_id' in vals:
                variant = self.env['product.product'].browse(vals['product_id'])
                print("variant",variant)
                note += f"The Variant changed to : {variant.name} \n"

            if 'code' in vals:
                note += f"The Code changed to : {vals['code']} \n"

            if 'type' in vals:
                type=dict(self._fields['type'].selection).get(vals['type'])
                note += f"The Type changed to : {type} \n"

            if 'bom_line_ids' in vals:
                for line in vals['bom_line_ids']:
                    print("checking bom line",line)
                    print("new line created")
                    if line[0] == 0:
                        note += f"New Bom line created.. \n"
                        rec_id = line[1]
                        print("Rec ID",rec_id)
                        if 'product_id' in line[2]:
                            product = self.env['product.product'].browse(line[2].get('product_id'))
                            note += f"Product : {product.name} \n"

                            qty = line[2].get('product_qty')
                            note += f"Quantity : {qty} \n"

                            unit_name = self.env['uom.uom'].browse(line[2].get('product_uom_id'))
                            print(unit_name,"unit name")
                            note += f"Unit : {unit_name.display_name} \n"

                    if line[0] == 1:
                        rec_id = line[1]
                        print("Rec ID", rec_id)
                        note += f"Bom line {rec_id} edited.... \n"

                        if 'product_id' in line[2]:
                            product = self.env['product.product'].browse(
                            line[2].get('product_id'))
                            note += f"Product : {product.name} \n"

                        if 'product_qty' in line[2]:
                            qty = line[2].get('product_qty')
                            note += f"Quantity : {qty} \n"

                        if 'product_uom_id' in line[2]:
                            unit_name = self.env['uom.uom'].browse(
                                line[2].get('product_uom_id'))
                            print(unit_name, "unit name")
                            note += f"Unit : {unit_name.display_name} \n"

                    if line[0] == 2:
                        print("line edited!!")
                        rec_id = line[1]
                        print("Rec ID", rec_id)
                        note += f"Bom line {rec_id} deleted.... \n"

                self.env['bom.tracker'].create({
                    'bom_id': rec.id,
                    'revision_number': len(rec.track_ids)+1,
                    'modified_by': self.env.user.id,
                    'modified_on': fields.Datetime.now(),
                    'change_notes': note})

        return super().write(vals)

    #     note.append("product changed to "+ str(vals['product_tmpl_id']))
    # print(note,"changed")
