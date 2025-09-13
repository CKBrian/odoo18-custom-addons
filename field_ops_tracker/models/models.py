# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FieldOpsTracker(models.Model):
    _name = 'field.opstracker'
    _description = 'Field Operations Tracker'

    name = fields.Char(required=True)
    # value = fields.Integer()
    # value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

