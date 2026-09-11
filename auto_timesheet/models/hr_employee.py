# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
   _inherit = 'hr.employee'

   add_timesheet = fields.Boolean(string="Add Timesheet",default=False)
