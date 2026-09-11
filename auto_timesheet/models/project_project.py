# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProjectProject(models.Model):
   _inherit = 'project.project'

   def action_generate_timesheet(self):
       print("time//")
       for rec in self:
           active_task = self.env['project.task'].search([('active','=',True),('project_id','=',rec.id)])
           print("active",active_task)

           employee = active_task.filtered(lambda l :l.user_ids.add_timesheet==True)
           print("emp",employee)


