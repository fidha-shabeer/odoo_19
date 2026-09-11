from odoo import models, fields

class CreditLimitReport(models.TransientModel):
    _name = 'credit.limit.report'

    partner_id = fields.Many2one('res.partner',string="Customer")

    def action_credit_limit_xlsx(self):
        print("printing////")