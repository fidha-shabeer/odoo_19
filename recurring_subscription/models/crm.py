from odoo import models, fields


class CrmLead(models.Model):
   _inherit = 'crm.lead'
   _unique_orderid = models.Constraint('UNIQUE(order_no)','This order no. already been registered')

   order_no = fields.Char(string="Order ID")