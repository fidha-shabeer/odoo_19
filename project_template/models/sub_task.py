# -*- coding: utf-8 -*-
from odoo import models, fields


class ProjectTaskTemplate(models.Model):
    _name = 'project.task.template'
    _description = 'Project Task Template'

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner')
    project_id = fields.Many2one('project.template',string='Project')
    parent_id = fields.Many2one('project.task.template', string='Parent Task')
