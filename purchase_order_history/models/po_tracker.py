# -*- coding: utf-8 -*-

from odoo import fields, models,api


class PoTracker(models.Model):
    _name = 'po.tracker'
    _description = 'PO Tracker'

    revision_number = fields.Integer('Revision Number')
    modified_by = fields.Many2one('res.users',string='User')
    modified_on = fields.Datetime(string='Date Time',default=fields.Datetime.now)
    change_notes = fields.Char(string='Change Notes')




