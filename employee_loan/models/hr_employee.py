# -*- coding: utf-8 -*-
from odoo import models, fields

class HrEmployee(models.Model):
   _inherit = 'hr.employee'

   loan_not_allowed = fields.Boolean(string="Loan Not Allowed")

