from odoo import models, api,fields

class QrCodeGenerator(models.AbstractModel):
    _name = 'report.qr_code_generator.qr_report'
    _description = 'qrcode Report Details'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['qr.generate.wizard'].browse(
            docids)
        print(docs,"docss")


        return {
            'doc_ids': docids,
            'doc_model': 'qr.generate.wizard',
            'docs': docs,
            'qr_code': data.get('qr_code',[]) if data else [],
            'text' : data.get('text','') if data else '',
        }