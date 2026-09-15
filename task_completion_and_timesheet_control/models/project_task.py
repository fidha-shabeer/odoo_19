from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = "project.task"

    def write(self, vals):
        print("self",self.stage_id.name)
        print("vals",vals)
        print(type(vals))
        stage = vals.get("stage_id")
        print("stage",stage)
        stage_id = self.env['project.task.type'].browse(stage)
        if stage_id.name == 'Done':
            print("stage_id", stage_id.name)
            print("yes in done")
            for rec in self:
                line_stages = rec.child_ids.stage_id.ids
                stages = self.env['project.task.type'].browse(line_stages)
                print("stages",stages)
                for stage in stages:
                    print("stage",stage.name)
                    if stage.name != 'Done':
                        print("validation error")
                        raise ValidationError("The sub tasks are not in done states")
        return super().write(vals)


                # print("line_stage_name",line_stages.name)
                # if line_stages. not in
                # for line in rec.child_ids:
                #
                #
                #     print("lines", line)
                #     print(line.stage_id.name)
                #     if line.stage_id.name != 'Done':
                #         raise ValidationError("Can't change state as the sub task is not is not in done stage")
                #     else:
                #         return res





                    # if line.stage_id.name != 'Done':
                    #     raise ValidationError("cant change state as the sub task is not in done state")
                    # else:
                    #     print("in done state")
                        # rec.stage_id= vals['stage_id']
                        # print("rec stage", rec.stage_id)
                    #     stage = rec.stage_id
                    #     print("stage",stage.name)
                    # if stage.name == 'Done':
                    #     print("it is in done stage")


        # if 'stage_id' in vals:
        #     for rec in self:
        #         stage = self.env['project.task.type'].browse(vals['stage_id'])
        #         print("stage name", stage.name)
        #         if stage.name == 'Done':
        #             for line in rec.child_ids:
        #                 print("line stage", line.stage_id)
        #                 if line.stage_id != stage:
        #                     print("not done")
        #                     raise ValidationError("cant change stage")
        #                 else:
        #                     for line in rec.child_ids:
        #                         for time in line.timesheet_ids:
        #                             timesheet = self.env['account.analytic.line'].sudo().create({
        #                                 'date': time.date,
        #                                 'employee_id': time.employee_id.id,
        #                                 'name': time.name,
        #                                 'unit_amount': time.unit_amount,
        #                             })


    #
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if 'timesheet_ids' not in vals:
    #             raise ValidationError("timesheet_ids is required")
    #     return super().create(vals_list)
