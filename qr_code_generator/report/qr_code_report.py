from odoo import models, api,fields

class QrCodeGenerator(models.AbstractModel):
    _name = 'report.qr_code_generator.qr_report'
    _description = 'qrcode Report Details'

    @api.model
    def _get_report_values(self, docids, data=None):
        qr_code = data.get('qr_code',
                                     []) if data else []
        print("qr_code", qr_code)

        return {
            'doc_model': 'qr.generate.wizard',
            'docs': qr_code,
        }