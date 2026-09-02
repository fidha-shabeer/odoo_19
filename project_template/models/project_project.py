# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def action_project_template(self):
        print("creating project template")
        for rec in self:
            template = self.env['project.template'].create({
                'name': rec.name,
                'partner_id': rec.partner_id.id,
            })
            for task in rec.task_ids:
                self.env['project.task.template'].create({
                    'name' : task.name,
                    'project_id': template.id,
                    'partner_id': task.partner_id.id,
                })