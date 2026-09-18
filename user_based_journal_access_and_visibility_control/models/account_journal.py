# -*- coding: utf-8 -*-
from odoo import fields, models
class AccountJournal(models.Model):
    _inherit = "account.journal"

    user_id = fields.Many2one("res.users",string="User",default=lambda self: self.env.user.partner_id.name)
    journal_ids = fields.Many2many("account.journal",string="Journals",related="user_id.journal_ids")



