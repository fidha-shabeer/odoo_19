# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectTemplate(models.Model):
    _name = 'project.template'
    _description = 'Project Template'

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner')
    task_ids = fields.One2many('project.task.template', 'project_id',string='Tasks')

    def action_create_project(self):
        print("creating project")
        for rec in self:
            project=self.env['project.project'].create({
                'name': rec.name,
                'partner_id': rec.partner_id.id,
            })
            for task in rec.task_ids:
                task= self.env['project.task'].create({
                    'name': task.name,
                    'project_id': project.id,
                    'partner_id': task.partner_id.id,})

                sub = self.env['project.task'].create({
                    'name': task.child_ids.name,
                    'partner_id': task.child_ids.partner_id.id,
                    'parent_id': task.id,

                })


                # for sub in task.child_ids:
                #     subtask = self.env['project.task'].create({
                #                 'name' : sub.name,
                #                 'partner_id' : sub.partner_id.id,
                #                 'project_id' : project.id,
                #                 'parent_id' : task.id,
                #             })


        return{
                'type': 'ir.actions.act_window',
                'res_model': 'project.project',
                'res_id': project.id,
                'view_mode': 'form',
            }

