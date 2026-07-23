from odoo import models,api
from odoo.exceptions import ValidationError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.constrains('unit_amount')
    def _check_hours_per_day(self):
        print("Hours per day")
        for rec in self:
            record = self.search([('date','=',rec.date),('task_id','=',rec.task_id)])
            total = sum(record.mapped('unit_amount'))
            print(total)
            print(record)
            # time = self.search([('date','=',rec.date)])
            if rec.task_id.hours_per_day < total:
                raise ValidationError("The time spent should not exceed the total hour per day")
            else:
                return True

