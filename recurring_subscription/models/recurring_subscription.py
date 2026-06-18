
from odoo import fields,models,api
from datetime import timedelta


class RecurringSubscription(models.Model):
    _name = "recurring.subscription"
    _description = "Recurring Subscription"
    _rec_name = "order_seq"

    stages_id = fields.Selection(selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')], string="State",
        default='draft')
    order_seq=fields.Char()
    establishment_id = fields.Char(string="Establishment ID")
    date = fields.Date(string="Date" , required=True)
    due_dates=fields.Date(string="Due Dates",compute="_compute_dates" , store=True)
    next_billing = fields.Date(string="Next Bill Date", compute="_compute_next_billing", store=True)
    is_leads = fields.Selection(selection=[("yes","Yes"),("no","No")], string="Is Lead?")
    partner_id = fields.Many2one("res.partner", string="Customer")
    description = fields.Text(string="Description")
    terms_condition = fields.Html(string="Terms and Condition")
    product_id = fields.Many2one("product.product", string="Product")
    recurring_amount = fields.Float(string="Recurring Amount")


    def create(self, vals_list):
        vals_list["order_seq"] = self.env["ir.sequence"].next_by_code('recsequence')
        return super(RecurringSubscription, self).create(vals_list)

    @api.depends("date")
    def _compute_dates(self):
        for rec in self:
            if rec.date:
                due_date_rec = fields.Datetime.from_string(rec.date) + timedelta(days=15)

                rec.due_dates = due_date_rec.date()

    @api.depends("date")
    def _compute_next_billing(self):
        for rec in self:
            if rec.date:
                billing_date_rec = fields.Datetime.from_string(rec.date) + timedelta(days=30)

                rec.next_billing = billing_date_rec.date()


