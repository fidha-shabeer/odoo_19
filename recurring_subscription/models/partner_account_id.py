# -*- coding: utf-8 -*-
from odoo import fields, models,api
from odoo.exceptions import ValidationError
import re


class Partner(models.Model):
    _name = "partner.account"
    _description = "Partner Account"
    _rec_name = "account_no"
    _inherit = ['mail.thread']

    _unique_account_no = models.Constraint('UNIQUE(account_no)','account no already registered')

    account_no = fields.Char(string="Account ID")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sequence = self.env['ir.sequence'].next_by_code('accountseq') or 000
            vals['account_no'] = f'@${sequence}'
        return super(Partner, self).create(vals_list)









