import json
import io
import xlsxwriter


from odoo.tools import json_default
from odoo import models, fields

class RecurringCreditReport(models.TransientModel):
    _name = 'recurring.credit.report'
    _description = 'Credit Report'

    sub_id = fields.Many2one('recurring.subscription',
                                      string='Subscription')
    state = fields.Selection(selection =[('pending', 'Pending'), ('confirmed', 'Confirmed'),
                                        ('first_approved', 'First Approved'),( 'fully_approved','Fully Approved'),('rejected', 'Rejected')])

    def action_credit_report(self):
        print("Credit Report")
        domain = []

        if self.sub_id and self.state:
            domain.extend([('recurring_sub_id', '=', self.sub_id.id),('state', '=', self.state)])
        elif self.sub_id:
            domain.append(('recurring_sub_id', '=', self.sub_id.id))
        elif self.state :
            domain.append(('state', '=', self.state))

        credits = self.env['recurring.credit'].search(domain)
        print("credits",credits)
        data = {
            'sub_id': self.sub_id.id,
            'state': self.state,
            'credits_ids' : credits.ids,
        }
        return self.env.ref(
            'recurring_subscription.action_subscription_credit_report_view').report_action(None, data=data)
    def action_credit_xlsx(self):
        data = {
            'sub_id': self.sub_id.id,
            'state': self.state,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'recurring.credit.report',
                     'options': json.dumps(data,
                                           default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Subscription Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print('gereteftfe')
        query = """ select c.recurring_sub_id,r.total_credits,r.order_seq,r.partner_id,r.recurring_amount,c.credit_amounts,r.recurring_amount - c.credit_amounts AS amount_pending ,c.state from recurring_credit AS c INNER JOIN recurring_subscription AS r ON c.recurring_sub_id = r.id """
        # self.env.cr.execute(query, (data['sub_id'],))
        param = []

        if data['sub_id']:
            query += """ WHERE c.recurring_sub_id = %s"""
            param.append(data['sub_id'])

        if data['state']:
            query += """ AND c.state = %s"""
            param.append(data['state'])

        self.env.cr.execute(query, param)

        records = self.env.cr.dictfetchall()
        print(records)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        sheet.set_column('A:F', 20)

        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, 'border': 2})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'border': 2})
        sub = workbook.add_format({'bold': True, 'align': 'center'})

        sheet.merge_range('B2:F3', 'CREDIT   EXCEL REPORT', head)

        subs = self.env['recurring.subscription'].search(
            [('id', '=', data['sub_id'])])
        print("subsss", subs)
        sub_filter = subs.mapped('order_seq')
        print("seq", sub_filter)
        l_sub = ''.join(sub_filter)
        if not l_sub:
            l_sub = "ALL"
        sheet.merge_range('A4:B4', 'Subscription -', sub)
        sheet.merge_range('C4:D4', l_sub, sub)


        states = data['state']
        if not states:
            states = 'ALL'
        sheet.merge_range('A5:B5', 'Status -', sub)
        sheet.merge_range('C5:D5', states, sub)

        sheet.write(7, 0, 'SL.No', cell_format)
        sheet.write(7, 1, 'Subscription', cell_format)
        sheet.write(7, 2, 'Customer', cell_format)
        sheet.write(7, 3, 'Credit Amount Applied', cell_format)
        sheet.write(7, 4, 'Amount Pending', cell_format)
        sheet.write(7, 5, 'State', cell_format)

        slno = 1
        row = 8
        for record in records:
            sheet.write(row,0, slno,txt)
            sheet.write(row,1,record['order_seq'],txt)
            sheet.write(row,2,record['partner_id'],txt)
            sheet.write(row,3,record['credit_amounts'],txt)
            sheet.write(row,4,record['amount_pending'],txt)
            sheet.write(row,5,record['state'],txt)

            slno += 1
            row += 1


        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

