from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        task = super().create(vals)

        employee = self.env["hr.employee"].search([
            ("skill_tag_ids", "in", task.tag_ids.ids)
        ], limit=1)

        if employee and employee.user_id:
            task.user_ids = [
                fields.Command.set([employee.user_id.id])
            ]

        return task

    def write(self, vals):

        if "stage_id" in vals:

            stage = self.env["project.task.type"].browse(
                vals["stage_id"]
            )

            if stage.name == "Done":

                for task in self:
                    hours = sum(
                        task.timesheet_ids.mapped("unit_amount")
                    )

                    if hours == 0:
                        raise ValidationError(
                            "Please enter timesheet hours before completing the task."
                        )

        result = super().write(vals)

        if "stage_id" in vals:

            for task in self:

                if task.stage_id.name == "In Progress":

                    for user in task.user_ids:

                        self.env["account.analytic.line"].create({
                            "name": "Task Started",
                            "date": fields.Date.today(),
                            "project_id": task.project_id.id,
                            "task_id": task.id,
                            "user_id": user.id,
                            "unit_amount": 0,
                        })

        return result