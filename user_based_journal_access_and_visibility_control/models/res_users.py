# -*- coding: utf-8 -*-
from odoo import fields, models
class ResUsers(models.Model):
    _inherit = "res.users"

    journal_ids = fields.Many2many(comodel_name='account.journal')

    def write(self, vals):
        print("self",self)
        print("vals",vals)
        print("val type",type(vals))
        list = []
        if 'journal_ids' in vals:
            for journal in vals['journal_ids']:
                journals = self.env['account.journal'].browse(journal[1])
                list.append(journals)
                print("journals",journals.name)
            print("list",list)
        return super().write(vals)

