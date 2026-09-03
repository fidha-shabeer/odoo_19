from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = "project.task"

    task_template_id = fields.Many2one("project.task.template")
    def action_task_template(self):
        print("creating task template..")
        for rec in self:
            print(rec)
            task_temp = self.env['project.task.template'].create({
                'name' : rec.name,
                'partner_id' : rec.partner_id.id,
                'project_id' : rec.project_id.id,
            })
            for sub in rec.child_ids:
                self.env['project.task.template'].create({
                    'name' : sub.name,
                    'project_id' : sub.project_id.id,
                    'parent_id' : task_temp.id,

            })
            rec.task_template_id = task_temp.id
            print("task",rec.task_template_id)

    def action_view_task_template(self):
        print("creating view task template..")
        self.ensure_one
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'project.task.template',
                'view_mode': 'list,form',
                'domain': [('id', '=', self.task_template_id.id)],
            }

