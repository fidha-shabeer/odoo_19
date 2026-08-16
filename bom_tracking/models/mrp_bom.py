# -*- coding: utf-8 -*-
from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    bom_history = fields.Char(string="BOM History")
    track_ids = fields.One2many(comodel_name="bom.tracker", inverse_name="bom_id", string="Tracks")

    def action_history(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'BOM History',
                'res_model': 'bom.tracker',
                'view_mode': 'list,form',
                'domain': [('bom_id', '=', rec.id)],
            }

    def write(self, vals):
        for rec in self:
            note = ''


            #if 'product_qty' in vals:
             #   note += "the product quantity changed to " + str(vals['product_qty']) + "\n"

            #if 'product_tmpl_id' in vals:
             #   product = self.env['product.template'].browse(vals['product_tmpl_id'])
              #  note += "the product changed to " + product.display_name + "\n"

           # if 'product_id' in vals:
               # variant = self.env['product.product'].browse(vals['product_id'])
             #   note += "product variant changed to %s" % variant.display_name + "\n"

           # if 'code' in vals:
              #  note += "the code changed to " + vals['code'] + "\n"

            #if 'type' in vals:
                #type = dict(self._fields['type']._description_selection(self.env)).get(vals['type'])
                #note += "the type changes to " + type + "\n"

            if 'bom_line_ids' in vals:
                print("in line.....",vals)
                for line in vals['bom_line_ids']:


                    if not line:
                        continue
                    if line[0] == 0:
                        if len(line)>2:
                            pro = self.env['product.product'].browse(line[2].get('product_id'))
                            qty =line[2].get('product_qty')
                            note += "new bom line created, \n"+f"the created record contains product {pro.name}\n"+f"the product qty is {qty}\n"

                    if line[0] == 1:
                        if len(line)>2:
                            id_line=line[1]
                            print("here",id_line)
                            pro = self.env['product.product'].browse(line[2].get('product_id'))
                            qty = line[2].get('product_qty')
                            note+= f"the record ID:{ pro.id}  is edited"+ f"the values changed are {pro.name}\n" + f"the product qty is {qty}\n"

                    if line[0] == 2:
                        if len(line)>1:
                            id_line =line[1]
                            print(id_line,"uhfuhr")
                            note += f"the record with ID {id_line}: is deleted"

                    if line[0]==3:
                        if len(line)>1:
                            id_line = line[1]
                            print(id_line,"uhfuhr")
                            note += f"the record with ID: is deleted"




            if note:
                self.env['bom.tracker'].create({
                    'bom_id': rec.id,
                    'modified_by': self.env.user.id,
                    'revision_number': len(rec.track_ids) + 1,
                    'modified_on': fields.Datetime.now(),
                    'change_notes': note, })

        return super().write(vals)

    #     note.append("product changed to "+ str(vals['product_tmpl_id']))
    # print(note,"changed")
