# -*- coding: utf-8 -*-
from odoo import fields,models

class CrmTeam(models.Model):
    _inherit = "crm.team"

    crm_state_id = fields.Many2one('crm.stage',string="CRM State")

