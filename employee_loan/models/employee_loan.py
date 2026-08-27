# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EmployeeLoan(models.Model):
    _name = "employee.loan"
    _description = "Employee Loan"

    name = fields.Char(default="New")
    loan_line_ids = fields.One2many("employee.loan.line", "loan_id",
                                    string="Loan Lines")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    installment_amount = fields.Float(string="Installment Amount")
    total_payable = fields.Float(string="Total Payable",
                                 compute="_compute_total_payable")
    loan_amount = fields.Float(string="Loan Amount")
    installment_count = fields.Integer(string="Installment Count")
    start_date = fields.Datetime(string="Start Date")
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('approved', 'Approved'),
                   ('ongoing', 'Ongoing'),
                   ('paid', 'Paid')],
        string="State", default='draft')
    loan_count = fields.Integer(string="Loan Count",
                                compute="_compute_loan_count")
    paid_amount = fields.Float(string="Paid Amount",
                               compute="_compute_paid_amount",store=True)

    balance_amount = fields.Float(string="Balance Amount",compute="_compute_balance_amount",store=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Sequence creation """
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env["ir.sequence"].next_by_code('loanseq')
        return super().create(vals_list)

    @api.onchange('loan_amount', 'installment_count')
    def _onchange_amount(self):
        if self.loan_amount or self.installment_count:
            if self.installment_count != 0:
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
            if rec.loan_amount < 1:
                raise ValidationError("Loan amount cannot be negative")
            else:
                rec.state = 'approved'

    def action_generate(self):
        print("generating")
        for rec in self:
            amount = rec.loan_amount / rec.installment_count
            for i in range(rec.installment_count):
                self.env['employee.loan.line'].create({
                    'amount': amount,
                    'loan_id': rec.id,
                })

    @api.depends('loan_line_ids')
    def _compute_loan_count(self):
        for rec in self:
            rec.loan_count = len(rec.loan_line_ids)
            print("loan_count", rec.loan_count)

    def action_smart_tab(self):
        for rec in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'INstallment',
                'res_model': 'employee.loan.line',
                'view_mode': 'list,form',
                'target': 'current',
                'domain': [('loan_id', 'in', rec.id)],

            }

    def action_pay(self):
        print("pay")
        for rec in self:
            first = rec.loan_line_ids.filtered(lambda line: not line.paid)[:1]
            print("print 1st", first)
            first.write({'paid': True})

            if not rec.loan_line_ids.filtered(lambda line: not line.paid):
                rec.write({'state': 'paid'})


    @api.depends('loan_line_ids')
    def _compute_paid_amount(self):
        for rec in self:
            if rec.loan_line_ids:
                rec.paid_amount = sum(rec.loan_line_ids.filtered(lambda line:line.paid).mapped('amount'))
                print("paid_amount", rec.paid_amount)

    @api.depends('total_payable','paid_amount')
    def _compute_balance_amount(self):
        for rec in self:
            if rec.loan_line_ids:
                rec.balance_amount=rec.total_payable - rec.paid_amount
                print("balance_amount", rec.balance_amount)