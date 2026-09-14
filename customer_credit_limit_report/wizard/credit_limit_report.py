from pydoc import text

from odoo import models, fields
import json
import io
import xlsxwriter
from odoo.tools import json_default
from datetime import datetime


class CreditLimitReport(models.TransientModel):
    _name = 'credit.limit.report'

    partner_id = fields.Many2one('res.partner', string="Customer")

    def action_credit_limit_xlsx(self):
        '''credit limit excel report'''
        print("printing////")
        print("customer", self.partner_id.id)
        data = {
            'partner_id': self.partner_id.id,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'credit.limit.report',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Customer Credit Limit Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        '''get xlsx report'''
        print('generating excel!!')

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        sheet.set_column('A:F', 20)

        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, 'border': 2})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format(
            {'font_size': '10px', 'align': 'center'})
        sub = workbook.add_format({'bold': True, 'align': 'center'})

        sheet.merge_range('B2:F3','CREDIT LIMIT EXCEL REPORT', head)

        customer_id = data['partner_id']
        print(customer_id)

        if not customer_id:
            print("no customer exist!!")
            customers = self.env['res.partner'].search([])
            print("customer", customers)
            customer_name = "ALL"
        else:
            customers = self.env['res.partner'].browse(customer_id)
            print(customers.display_name)
            customer_name = customers.display_name
        print(customer_name)


        date = fields.Date.today()
        print(date)
        print(type(date))


        sheet.merge_range('A4:B4', 'Report Date: ', sub)
        sheet.merge_range('C4:D4',fields.Date.to_string(date), txt)

        sheet.merge_range('A5:B5', 'Customer Name: ', sub)
        sheet.merge_range('C5:D5', customer_name, txt)

        sheet.write(7, 0, 'Email', cell_format)
        sheet.write(7, 1, 'Phone', cell_format)
        sheet.write(7, 2, 'Due Amount', cell_format)

        row = 8
        for customer in customers:

            sheet.write(row, 0, customer.email, txt)
            sheet.write(row, 1, customer.phone, txt)
            sheet.write(row, 2, customer.credit, txt)

            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
