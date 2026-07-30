import json
from odoo import http
from odoo.http import content_disposition, request,serialize_exception
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    """Xlsx Report controller"""
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'],
                csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name):
        """xlsx report"""
        """ Return data to python file passed from the javascript"""
        session_unique_id = request.session.uid
        print('session uid',session_unique_id)
        report_object = request.env[model].with_user(session_unique_id)
        print('report_object',report_object)
        options = json.loads(options)
        print('options',options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_object.get_xlsx_report(options, response)
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            se = serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))