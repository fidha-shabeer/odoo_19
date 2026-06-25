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

    @api.constrains('account_no')
    def _check_accountid(self):
        for record in self:
            if record.account_no:
                pattern1 = '[a-zA-z]{3,}'
                pattern2 = '(?=.\d{3,})'
                pattern3 = '(?=.*[@.#$!%?&]{2,})'
                if not re.findall(pattern1, record.account_no):
                    raise ValidationError('Account ID not valid')
                if not re.findall(pattern2, record.id_establishments):
                    raise ValidationError('Account ID not valid')
                if not re.findall(pattern3, record.id_establishments):
                    raise ValidationError('Account ID not valid')










