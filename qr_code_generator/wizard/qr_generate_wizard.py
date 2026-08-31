from odoo import models, fields, api
import base64
import io
import qrcode

class QrGenerateWizard(models.TransientModel):
   _name = 'qr.generate.wizard'
   _description = 'Wizard for QR Generation'

   text = fields.Char(string='Text to generate QR Code')
   qr_code = fields.Binary("QR Code", compute='_generate_qr_code',store=True)

   @api.depends('text')
   def _generate_qr_code(self):
      print("computingg!!")
      for rec in self:
         text = rec.text
         print(rec.qr_code)
         if qrcode and base64:
            qr = qrcode.QRCode(
               version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
            )
            qr.add_data(text)
            print(rec.text,"printing given text")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            temp = io.BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            rec.update({'qr_code': qr_image})



   @api.model_create_multi
   def action_download(self,args):
      print("button clicked!!")
      for rec in self:
         return {
               'name': 'QrCode Download',
               'type': 'ir.actions.act_url',
               'url': '/web/content/model.name/%s/contract_template/contract_template.xls?download=true' %(self.id),
               'target': 'self',
            }

         # 'type': "ir.actions.act_window",
         # 'name': "Generate QR Code",
         # 'res_model': "qr.generate.wizard",
         # 'view_mode': "form",
         # 'target': "new",}



   @api.model
   def action_reset(self,args):
      print("button reset clicked!!")
      return {
         'type': "ir.actions.act_window",
         'name': "Generate QR Code",
         'res_model': "qr.generate.wizard",
         'view_mode': "form",
         'target': "new", }


   def action_pdf(self):
      print("PDF button clicked!!")
      self.ensure_one()
      data = {
         'qr_code': self.qr_code,
      }
      return self.env.ref(
         'qr_code_generator.action_qr_pdf_report'
      ).report_action(None, data = data)