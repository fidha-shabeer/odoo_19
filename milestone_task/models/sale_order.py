# -*- coding: utf-8 -*-
from odoo import fields,models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    projects = fields.Char(string="Projects")
    projects_id = fields.Many2one('project.project',string="Project")

    def action_create_project_1(self):
        for rec in self:
            if not rec.project_id:
                project = self.env['project.project'].create({
                        'name': rec.name,
                        'partner_id': rec.partner_id.id,
                })
            rec.projects_id = project.id

            for l in rec.order_line:
                task = self.env['project.task'].search([('project_id', '=', project.id),('name','=',f"Milestone {l.milestone}" )])
                if not task:
                    task= self.env['project.task'].create({
                        'name': f"Milestone {l.milestone}",
                        'project_id' : project.id,
                         })

                child = self.env['project.task'].create({
                        'name': f"Milestone {l.milestone}-{l.product_template_id.display_name}",
                        'project_id':project.id,
                        'parent_id': task.id,
                    })

            return True

    def action_project_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project',
            'view_mode': 'list',
            'res_model': 'project.project',
            'res_id': self.projects_id.id,
            'target': 'current',
            'domain': [('partner_id', 'in' ,self.id)],
            }
