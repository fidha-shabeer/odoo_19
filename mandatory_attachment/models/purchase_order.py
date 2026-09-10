from odoo import models, fields,api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    attachment_ids = fields.Many2many(comodel_name='ir.attachment',string='Attachments')

    def button_confirm(self):
        print("workinggg..........")

        params = self.env['ir.config_parameter'].sudo()
        print("params",params)
        is_required = params.get_param('mandatory_attachment.is_required_attachment')
        print(is_required)

        if is_required:
            for rec in self:
                attached = self.env['ir.attachment'].sudo().search([('res_model', '=', 'purchase.order'),
                    ('res_id', '=', rec.id)])
                print("attach",attached)
                if not attached:
                    raise ValidationError('Mandatory Attachment is Required')
                for attach in attached:
                    if attach.mimetype not in ('image/jpeg','application/pdf'):
                        raise ValidationError('Attach the jpg/pdf files!')

                    # if attach.mimetype != 'image/jpeg' or attach.mimetype != 'application/pdf':

            # if not rec.attachment_ids:
            #     raise ValidationError('Mandatory Attachment is Required')

        return super().button_confirm()

    # @api.constrains('attachment_ids')
    # def _check_attachment_ids(self):
    #     if not self.attachment_ids:
    #         raise ValidationError('Mandatory Attachment is Required')