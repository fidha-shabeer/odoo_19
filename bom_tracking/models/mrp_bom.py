# -*- coding: utf-8 -*-
from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    bom_history = fields.Char(string="BOM History")

    def action_history(self):
        print("history loading...")
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'BOM History',
                'res_model': 'bom.tracker',
                'view_mode': 'list,form',
                'domain': [('bom_id', 'in', rec.id)],
            }

    def write(self, vals: dict[str, str]):
        for rec in self:
            print("sdfghjkl", vals)
            note = ''
            if vals['product_qty']:
                note += str(vals['product_qty'])
                print(note, "fghjk")
                # note = " ".join(note)
                print(note)

                self.env['bom.tracker'].create({
                    'bom_id': rec.id,
                    'revision_number': 1,
                    'modified_by': self.env.user.partner_id,
                    'modified_on': fields.Datetime.now(),
                    'change_notes': note, })

        return super().write(vals)

    #     note.append("product changed to "+ str(vals['product_tmpl_id']))
    # print(note,"changed")
