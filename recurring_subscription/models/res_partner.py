from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
   _inherit = 'res.partner'
   _rec_name = 'account_no'

   _unique_establishment_id = models.Constraint('UNIQUE(id_establishments)',
                                          'Id already registered')

   id_establishments =  fields.Char(string="Establishment ID")
   account_no = fields.Many2one('partner.account',ondelete='cascade', string="Account ID")


   @api.constrains('id_establishments')
   def _check_establishments(self):
      for record in self:
         if record.id_establishments:
            pattern1 = '[a-zA-z]{3,}'
            pattern2 = '(?=.\d{3,})'
            pattern3 = '(?=.*[@.#$!%?&]{2,})'
            if not re.findall(pattern1, record.id_establishments):
               raise ValidationError('Establishment ID not valid')
            if not re.findall(pattern2, record.id_establishments):
               raise ValidationError('Establishment ID not valid')
            if not re.findall(pattern3, record.id_establishments):
               raise ValidationError('Establishment ID not valid')

   @api.model_create_multi
   def create(self, vals_list):
      records = super().create(vals_list)
      for rec in records:
         acc = self.env['partner.account'].create({})
         rec.account_no = acc
      return records

























