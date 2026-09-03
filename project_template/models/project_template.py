# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectTemplate(models.Model):
    _name = 'project.template'
    _description = 'Project Template'

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner')
    task_ids = fields.One2many('project.task.template', 'project_id',string='Tasks')
    project_temp_id = fields.One2many('project.project',inverse_name='template_id',ondelete='cascade')

    def action_create_project(self):
        print("creating project")
        for rec in self:
            project=self.env['project.project'].create({
                'name': rec.name,
                'partner_id': rec.partner_id.id,
                'template_id': rec.id,

            })
            for task in rec.task_ids:
                if not task.parent_id:
                    parent_task= self.env['project.task'].create({
                        'name': task.name,
                        'project_id': project.id,
                        'partner_id': task.partner_id.id,})

                    for sub in task.child_ids:
                        subtask = self.env['project.task'].create({
                                    'name' : sub.name,
                                    'partner_id' : sub.partner_id.id,
                                    'parent_id' : parent_task.id,
                                })


        return{
                'type': 'ir.actions.act_window',
                'res_model': 'project.project',
                'res_id': project.id,
                'view_mode': 'form',
            }

    def action_view_project(self):
        print("viewing project")
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.project',
                'view_mode': 'list,form',
                'domain': [('template_id','=',rec.id)],
            }
