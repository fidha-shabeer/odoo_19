# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
   _inherit = 'project.task'

   allowed_hours = fields.Float(string="allowed hours")
   total_logged_hrs = fields.Float(
       string="Total Logged Hours",
       compute="_compute_total_logged_hrs",
       store=True
   )

   over_budget = fields.Boolean(
       string="Over Budget",
       compute="_compute_over_budget",
       store=True)

   @api.depends("timesheet_ids.unit_amount")
   def _compute_total_logged_hrs(self):
       for task in self:
           task.total_logged_hrs = sum(
               task.timesheet_ids.mapped("unit_amount")
           )

   @api.depends("total_logged_hrs", "allowed_hours")
   def _compute_over_budget(self):
       for task in self:
           task.over_budget = (
                   task.allowed_hours > 0 and
                   task.total_logged_hrs > task.allowed_hours * 1.20
           )
