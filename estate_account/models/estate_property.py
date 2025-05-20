# -*- coding: utf-8 -*-

from odoo import Command, models, fields, api
from odoo.exceptions import UserError


class EstateAccount(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        """ Override the action_sold method to return the super call"""
        print("\n -----\n✅ DEBUG: estate_account override of action_sold() was called\n -----\n")
        res = super().action_set_sold()
        res
        account_move = self.env['account.move']

        sale_journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1) 
        if sale_journal:
            for record in self:
                if not record.buyer_id:
                    raise UserError('A buyer must be specified before selling a property')
                account_move.create({
                    'partner_id': record.buyer_id.id,
                    'journal_id': sale_journal.id,
                    'move_type': 'out_invoice',
                    'line_ids': [
                        Command.create({
                            'name': '6% Commission',
                            'quantity': 1,
                            'price_unit': record.selling_price * 0.06,	
                        }),
                        Command.create({
                            'name': 'Administrative Fees',
                            'quantity': 1,	
                            'price_unit': 100.0,
                        }),
                    ]
                })
            
        else:
            raise UserError('No sale journal found')

        return res
