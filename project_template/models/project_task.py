from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = "project.task"

    def action_task_template(self):
        print("creating task template..")
        for rec in self:
            task_temp = self.env['project.task.template'].create({
                'name' : rec.name,
                'partner_id' : rec.partner_id.id,
                'project_id' : rec.project_id.id,
            })

