# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Partner(models.Model):
    _inherit = 'res.partner'

    author =  fields.Boolean('is an Author', default=False)
    publisher =  fields.Boolean('is a Publisher', default=False)
    rental_ids = fields.One2many(
        'library.rental',
        'customer_id',
        string='Rentals')
    book_ids = fields.Many2many(
        comodel_name="product.product",
        string="Books",
        domain=[('book','=',True), ],
    )
    nationality_id = fields.Many2one(
        'res.country',
        'Nationality',
    )
    payment_ids = fields.One2many(
        'library.payment',
        'customer_id',
        string='Payment')
    birthdate =  fields.Date('Birthdate',)
    
    payment_count = fields.Integer(string="Payment Number", compute="_compute_payment_count")
    
    @api.multi
    def _compute_payment_count(self):
        for partner in self:
            partner.payment_count = len(partner.payment_ids)
            
    @api.multi
    def action_open_payment(self):
        self.ensure_one()
        if self.payment_ids:
            return({
                'type' : 'ir.actions.act_window',
                'name' : _('Rental Payment'),
                'view_mode': 'tree,form',
                'res_model': 'library.payment',
                'res_id' : self.payment_ids
            })
            
        
            
