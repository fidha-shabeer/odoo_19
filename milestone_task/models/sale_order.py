# -*- coding: utf-8 -*-
from odoo import fields, models
# from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_id = fields.Many2one("project.project", string="Project")
    project_task_id = fields.Many2one("project.task", string="Task")

    def action_create_project_1(self):
        print('project creation button clicked')
        for rec in self:
            if not rec.project_id:
                project_name = rec.name
                project = self.env['project.project'].create({
                    'name': project_name,
                    'partner_id': rec.partner_id.id,
                    'task_ids': [(fields.Command.create({
                    'name': f"Milestone {rec.order_line.milestone}",
                        'child_ids' : [(fields.Command.create({
                            'name': f"Milestone {rec.order_line.milestone}-{rec.order_line.product_template_id.display_name}",

                        }))],
                }))],

            })
                rec.project_id = project.id
            return True

            # task_name = self.env['project.task']
            # project_task = self.env['sale.order.line']
            #
            # project_task = self.env['project.task'].create({
            #     'name': task_name,
            #     # 'partner_id': rec.partner_id.id,
            #
            # })
            #
            # rec.project_task_id = project_task.id

