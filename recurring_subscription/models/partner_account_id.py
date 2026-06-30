# -*- coding: utf-8 -*-
from odoo import fields, models,api
import random
import string


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
            random_seq1 = ''.join(random.choices(string.ascii_letters, k=(3)))
            random_seq2 = ''.join(random.choices(string.digits, k=(3)))
            random_seq3 = ''.join(random.choices(string.punctuation, k=(2)))
            vals['account_no'] = random_seq1+random_seq2+random_seq3

        return super(Partner, self).create(vals_list)









