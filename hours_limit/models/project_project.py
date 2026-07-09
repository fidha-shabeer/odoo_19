# -*- coding: utf-8 -*-
from odoo import fields, models, api
# from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    hours_per_day = fields.Float(compute="_compute_hours_per_day", string="Hours per Day", store=True)


    # r=self.env["account.analytic.line"].search([("project_id", "=", self.id)])
    # @api.constrains('hours_per_day')
    # def _check_unit_amount(self):
    #     print("1234")
    #     for rec in self:
    #     # r = self.env["account.analytic.line"].search([])
    #         if rec.timesheet_ids.unit_amount:
    #             if rec.timesheet_ids.unit_amount >= rec.hours_per_day:
    #         # if rec.unit_amount > self.hours_per_day:
    #                 raise ValidationError('should not exceed the hours per day!!!')

    @api.depends('timesheet_ids.unit_amount')
    def _compute_hours_per_day(self):
        for rec in self:
            rec.hours_per_day = 8
            if rec.timesheet_ids.unit_amount > 8:
                raise ValidationError("The time spent should not exceeds 8")
            else:
                return True
