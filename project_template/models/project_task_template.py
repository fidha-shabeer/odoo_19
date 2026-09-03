# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectTaskTemplate(models.Model):
    _name = 'project.task.template'
    _description = 'Project Task Template'

    name = fields.Char(required=True)
    project_temp_id = fields.Many2one('project.template', string='Project')
    partner_id = fields.Many2one('res.partner',related='project_id.partner_id')
    parent_id = fields.Many2one('project.task.template', string='Parent Task',)
    child_ids = fields.One2many('project.task.template', 'parent_id', string="Sub-tasks")
    task_id = fields.Many2one('project.task', string='Task')
    project_id = fields.Many2one('project.project', string='Project')

    def button_create_task(self):
        print("create task")
        for rec in self:
            if not rec.parent_id:
                task = self.env['project.task'].create({
                    'name': rec.name,
                    'partner_id': rec.partner_id.id,
                    'project_id': rec.project_id.id,
                })

                for sub in rec.child_ids:
                    self.env['project.task'].create({
                        'name': sub.name,
                        'parent_id': task.id,
                        'partner_id': sub.partner_id.id,
                    })

                rec.task_id = task.id
                print('rec',rec.task_id)

                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'project.task',
                    'res_id': task.id,
                    'view_mode': 'form',
                        }

    def action_view_task(self):
        print("view task")
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.task',
                'view_mode': 'list,form',
                'domain': [('id','=',rec.task_id.id)],
            }
