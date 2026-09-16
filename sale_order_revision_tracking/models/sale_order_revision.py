# -*- coding: utf-8 -*-

from odoo import fields, models,api


class SaleOrderRevision(models.Model):
    _name = 'sale.order.revision'

    sale_id = fields.Many2one(comodel_name='sale.order',string='Sale Order')
    revision_number = fields.Integer('Revision Number')
    modified_by = fields.Many2one('res.users',string='User')
    modified_on = fields.Datetime(string='Date Time',default=fields.Datetime.now)
    change_notes = fields.Char(string='Change Notes')




