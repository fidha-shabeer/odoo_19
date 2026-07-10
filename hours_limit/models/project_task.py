# -*- coding: utf-8 -*-
from odoo import fields, models

class ProjectTask(models.Model):
    _inherit = "project.task"

    hours_per_day = fields.Float(string="Hours per Day")

