# -*- coding: utf-8 -*-

from odoo import fields, models,api


class BomTracker(models.Model):
    _name = 'bom.tracker'
    _description = 'BOM Tracker'

    bom_id = fields.Many2one('mrp.bom', string='BOM')
    revision_number = fields.Integer('Revision Number')
    modified_by = fields.Many2one('res.users',string='User')
    modified_on = fields.Datetime(string='Date Time',default=fields.Datetime.now)
    change_notes = fields.Text(string='Change Notes')




