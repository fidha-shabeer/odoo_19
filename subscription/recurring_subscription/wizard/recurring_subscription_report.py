import json
import io
from odoo.tools import json_default, html2plaintext
from datetime import timedelta
from odoo import models, fields
# from odoo.tools import text_from_html
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class RecurringSubscriptionReport(models.TransientModel):
    _name = 'recurring.subscription.report'
    _description = 'Subscription Report'

    subscription_ids = fields.Many2many('recurring.subscription',
                                      string='Subscription')
    report_type = fields.Selection(
        selection=[('daily', 'Daily'), ('weekly', 'Weekly'),
                   ('monthly', 'Monthly'), ('yearly', 'Yearly')],
        string='Report Type')

    def action_sub_report(self):
        '''wizard to create subscription report'''
        print("its working")

        domain = []
        today = fields.Date.today()
        for rec in self:
            if rec.subscription_ids:
                domain.append(('id', '=', rec.subscription_ids))
            elif rec.report_type == 'daily':
                domain.append(('date','==',today))
            elif rec.report_type == 'weekly':
                start_date = today - timedelta(today.weekday())
                end_date = start_date + timedelta(days=6)
                domain.extend([('date', '>=', start_date), ('date', '<=', end_date)])
            elif rec.report_type == 'monthly':
                start_date = today.replace(day=1)
                end_date = start_date + timedelta(days=30)
                domain.extend([('date', '>=', start_date), ('date', '<=', end_date)])
            elif rec.report_type == 'yearly':
                start_date = today.replace(month=1, day=1)
                end_date = start_date + timedelta(days=365)
                domain.extend([('date', '>=', start_date), ('date', '<=', end_date)])
            subscriptions = self.env['recurring.subscription'].search(domain)
            data = {
                'subscription_id': rec.subscription_ids.ids,
                'report_type': rec.report_type,
                'subscriptions_ids': subscriptions.ids,
                }

            return self.env.ref(
                'recurring_subscription.action_subscription_report'
            ).report_action(None, data = data)


    def action_print_xlsx(self):
        print("excel working....")

        data = {
                'subscription_ids': self.subscription_ids.ids,
                'report_type': self.report_type,
            }
        return{
                'type': 'ir.actions.report',
                'data' : {'model': 'recurring.subscription.report',
                'options': json.dumps(data,default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Subscription Excel Report',
                    },
            'report_type' : 'xlsx',
            }

    def get_xlsx_report(self, data, response):
        print('gereteftfe')

        query =  """ select r.order_seq,r.recurring_amount,r.status,r.terms_condition, r.total_credits,
                 p.name AS customer,pro.default_code AS product from recurring_subscription AS r INNER JOIN res_partner AS p ON p.id = r.partner_id  INNER JOIN product_product AS pro ON pro.id = r.product_id WHERE 1=1
                 """

        # """ select r.order_seq,r.recurring_amount,r.status,r.terms_condition, r.total_credits,
        #         p.name AS customer,pro.default_code, pt.name ->> 'en_US' AS product from recurring_subscription AS r INNER JOIN res_partner AS p ON p.id = r.partner_id  INNER JOIN product_product AS pro ON pro.id = r.product_id INNER JOIN product_template as pt ON pt.id = pro.id  WHERE 1=1
        #         """

        param = []
        today = fields.Date.today()

        if data['subscription_ids']:
            query += """ AND r.id = ANY(%s)"""
            param.append(data['subscription_ids'])

        if data['report_type'] == 'daily':
            query += """ AND date = %s """
            param.append(today)

        elif data['report_type'] == 'weekly':
            start_date = today - timedelta(today.weekday())
            end_date = start_date + timedelta(days=6)
            query += """ AND date BETWEEN %s AND %s"""
            param.extend([start_date,end_date])

        elif data['report_type'] == 'monthly':
            start_date = today.replace(day=1)
            end_date = start_date + timedelta(days=30)
            query += """ AND date BETWEEN %s AND %s"""
            param.extend([start_date, end_date])

        elif data['report_type'] == 'yearly':
            start_date = today.replace(day=1,month=1)
            end_date = start_date + timedelta(month=12,days=31)
            query += """ AND date BETWEEN %s AND %s """
            param.extend([start_date,end_date])

        self.env.cr.execute(query,param)
        recordz = self.env.cr.dictfetchall()
        print("recorszzz --->", recordz)

        latest_terms = self.env['recurring.subscription'].search([],
                                                                 order='order_seq desc',
                                                                 limit=1)
        print("latest_terms", latest_terms)

        latest = latest_terms.terms_condition
        print("latest", latest)

        to_text = html2plaintext(latest)
        print("to_text", to_text)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        sheet.set_column('A:G',20)

        cell_format = workbook.add_format(
                    {'font_size': '12px', 'align': 'center' , 'bold': True, 'border':2})
        head = workbook.add_format(
                    {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format(
                    {'font_size': '10px', 'align': 'center', 'border':2})
        sub = workbook.add_format({'bold': True, 'align': 'center'})



        sheet.merge_range('A1:G2', 'SUBSCRIPTION EXCEL REPORT', head)

        subs = self.env['recurring.subscription'].search([('id','=',data['subscription_ids'])])
        print("subsss",subs)
        sub_filter = subs.mapped('order_seq')
        print("seq",sub_filter)
        l_sub = ''.join(sub_filter)
        if not l_sub:
            l_sub = "ALL"

        sheet.merge_range('A3:B3', 'Subscription -',sub)
        sheet.merge_range('C3:D3',l_sub,sub)

        type = data['report_type']
        print("TYPE: ",type)
        if not type:
            type = "ALL"

        sheet.merge_range('A4:B4', 'Report Type -',sub)
        sheet.merge_range('C4:D4',type,sub)


        sheet.write(8,0,'SL NO',cell_format)
        sheet.write(8,1,'Name',cell_format)
        sheet.write(8,2,'Customer',cell_format)
        sheet.write(8,3,'Product',cell_format)
        sheet.write(8,4,'Amount',cell_format)
        sheet.write(8,5,'Total Credit Amount',cell_format)
        sheet.write(8,6,'State',cell_format)

        sl = 1
        row = 9
        for rec in recordz:
            sheet.write(row,0,sl,txt)
            sheet.write(row,1,rec['order_seq'],txt)
            sheet.write(row,2,rec['customer'],txt)
            sheet.write(row,3,rec['product'],txt)
            sheet.write(row,4,rec['recurring_amount'],txt)
            sheet.write(row,5,rec['total_credits'],txt)
            sheet.write(row,6,rec['status'],txt)
            row +=1
            sl +=1

        sheet.write(row+5,2,to_text)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

