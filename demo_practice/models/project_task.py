from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model_create_multi
    def create(self,vals_list):
        print("vals_list",vals_list)
        task = super().create(vals_list)
        for vals in vals_list:
            tags_ids = vals.get('tag_ids')
            print("tags_ids",tags_ids)
            tags = self.env['project.tags'].browse(tags_ids[0])
            print("tag",tags)
            tg = tags.mapped('name')
            print("tg",tg)
            for t in tg:
                print("t",t)
                emp = self.env['hr.employee'].search([('skills_ids','in',tags.ids)])
                print("emp",emp)
                employee = emp.mapped('employee_id')
                print("emp",employee.name)
                if employee and employee.user_id:
                    task.user_ids = [fields.Command.set([employee.id])]

            return task



