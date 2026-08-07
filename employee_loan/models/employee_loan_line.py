# -*- coding: utf-8 -*-
from odoo import fields,models,api
class EmployeeLoan(models.Model):
    _name = "employee.loan.line"
    _description = "Employee Loan Line"

    loan_id = fields.Many2one('employee.loan',string="Loan")
    date = fields.Datetime(string="Loan")
    amount = fields.Float(string="Installment Amount")
    paid=fields.Boolean(string="Paid")
