from odoo import models, fields, api
import base64
import io
import qrcode
from PIL import Image

class QrGenerateWizard(models.TransientModel):
   _name = 'qr.generate.wizard'
   _description = 'Wizard for QR Generation'
   _rec_name = 'text'

   text = fields.Char(string='Text to generate QR Code')
   qr_code = fields.Binary("QR Code", compute='_generate_qr_code',store=True)
   image = fields.Image()
   filename = fields.Char(string='Name',default='image.png')

   @api.depends('text')
   def _generate_qr_code(self):
      print("computingg!!")
      for rec in self:

         if rec.text == False:
            return False

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
            rec.image = qr_image

            rec.write({'qr_code': qr_image,
                        'image': qr_image,}
                       )


   @api.model
   def action_download(self,args):
      print("button clicked!!")
      self.env.cr.commit()
      context = self.env.context
      print(context)
      idd = self.id
      print(idd,"iif")
      rec_id =self.env['qr.generate.wizard'].browse(self.env.context.get('uid'))
      print(rec_id,"id")

      return{
         'type': 'ir.actions.client',
         'tag': 'display_notification',
         'params': {
            'type': 'saving',
            'message': 'Saved',}

         }


   @api.model
   def action_reset(self,args):
      self.ensure_one
      return {
            'type': "ir.actions.act_window",
            'name': "Generate QR Code",
            'res_model': "qr.generate.wizard",
            'res_id': self.id,
            'view_mode': "form",
            'target': "new",
         }



   def action_pdf(self):
      print("PDF button clicked!!")
      self.ensure_one()

      return self.env.ref(
         'qr_code_generator.action_qr_pdf_report'
      ).report_action(self)