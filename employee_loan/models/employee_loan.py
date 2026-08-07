# -*- coding: utf-8 -*-
from odoo import fields,models,api
from odoo.exceptions import ValidationError


class EmployeeLoan(models.Model):
    _name = "employee.loan"
    _description = "Employee Loan"

    name = fields.Char(default="New")
    loan_line_ids = fields.One2many("employee.loan.line", "loan_id", string="Loan Lines")
    employee_id = fields.Many2one('hr.employee',string="Employee")
    installment_amount = fields.Float(string="Installment Amount")
    total_payable = fields.Float(string="Total Payable",compute="_compute_total_payable" )
    loan_amount = fields.Float(string="Loan Amount")
    installment_count = fields.Integer(string="Installment Count")
    start_date = fields.Datetime(string="Start Date")
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('approved', 'Approved'), ('ongoing', 'Ongoing'),
                   ('paid', 'Paid')],
        string="State", default='draft')
    loan_count = fields.Integer(string="Loan Count", compute="_compute_loan_count")

    @api.model_create_multi
    def create(self, vals_list):
        """Sequence creation """
        for vals in vals_list:
            if vals.get('name','New') == 'New':
                vals['name'] = self.env["ir.sequence"].next_by_code('loanseq')
        return super().create(vals_list)

    @api.onchange('loan_amount','installment_count')
    def _onchange_amount(self):
        if self.loan_amount or self.installment_count:
            if self.installment_count!=0:
                self.installment_amount = self.loan_amount / self.installment_count
            else:
                self.installment_amount = 0

    @api.depends('loan_amount')
    def _compute_total_payable(self):
        for rec in self:
            rec.total_payable = rec.loan_amount

    def action_approve(self):
        print("clicked")
        for rec in self:
            if rec.loan_amount<1:
                raise ValidationError("Loan amount cannot be negative")
            else:
                rec.state = 'approved'

    @api.depends('loan_line_ids')
    def _compute_loan_count(self):
        for rec in self:
            rec.loan_count = len(rec.loan_line_ids)
            print("loan_count", rec.loan_count)

    
