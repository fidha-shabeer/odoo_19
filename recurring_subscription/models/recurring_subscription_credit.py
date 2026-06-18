from odoo import fields, models

class RecurringSubscriptionCredit(models.Model):
    _name="recurring.credit"
    _description = "Recurring Subscription Credit"
    _rec_name = "recurring_sub"

    recurring_sub=fields.Many2one("recurring.subscription",string="Recurring Subscription")
    partner = fields.Many2one("res.partner",string="Recurring Subscription Partner")
    credit_amount = fields.Float(string="Credit Amount", required=True)
    states_id = fields.Selection(selection=[('pending', 'Pending'), ('confirmed', 'Confirmed'),('first approved', 'First Aprroved'),( 'fully approved','Fully Approved'),('rejected', 'Rejected')])
    period = fields.Datetime(string="Period")
