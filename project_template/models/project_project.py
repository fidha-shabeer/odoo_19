# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    template_id = fields.Many2one(comodel_name='project.template')

    def action_project_template(self):
        print("creating project template")
        for rec in self:
            template = self.env['project.template'].create({
                'name': rec.name,
                'partner_id': rec.partner_id.id,
            })
            for task in rec.task_ids:
                if not task.parent_id:
                    p_task = self.env['project.task.template'].create({
                        'name': task.name,
                        'project_id': template.id,
                        'partner_id': task.partner_id.id,
                    })
                    for child in task.child_ids:
                        child=self.env['project.task.template'].create({
                            'name': child.name,
                            'parent_id': p_task.id,
                        })
                    for c in child.child_ids:
                        subs1=self.env['project.task.template'].create({
                            'name': c.name,
                            'parent_id': child.id,
                        })
                    for n in c.child_ids:
                        print(n,'nothinggg')



            self.template_id = template.id
            print("template", rec.template_id)

    def action_view_project_template(self):
        print("creating project template")
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.template',
                'view_mode': 'list,form',
                'domain': [('id', '=', self.template_id.id)],
            }
