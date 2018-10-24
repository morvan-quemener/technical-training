# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date

class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'
    _order = "rental_date desc,return_date desc"

    customer_id = fields.Many2one(
        'res.partner',
        'Customer',
        domain=[('customer','=',True), ],
        required=True,
    )
    book_id = fields.Many2one(
        'product.product',
        'Book',
        domain=[('book','=',True)],
        required=True,
    )
    rental_date =  fields.Date(string='Rental date', required=True, default=lambda self: fields.Date.today())
    return_date =  fields.Date(string='Return date', required=True)
    
    @api.multi
    def action_return(self):
        for rental in self:
            rental.return_date = date.today()
            nbday = (rental.return_date-rental.rental_date).days+1
            tarif = float(self.env['ir.config_parameter'].get_param('library.daily_price'))
            due = nbday * tarif
            payment = self.env['library.payment'].create({
                'payment_date' : date.today(),
                'payment_amount' : due,
                'rental_id' : rental.id})            
            return({
                'type' : 'ir.actions.act_window',
                'name' : _('Rental Payment'),
                'view_mode': 'form',
                'res_model': 'library.payment',
                'res_id' : payment.id
            })
            
#    @api.multi
#    def action_lost(self):
#        for rental in self:
#            rental.book_id


class Payment(models.Model):
    _name = 'library.payment'
    _description = 'Rental payment'
    _order = "book_id, payment_date desc, customer_id"
    
    payment_date = fields.Date(String="Payment Date", required=True, readonly=True)
    payment_amount = fields.Float(String="Payment Amount", required=True)
    rental_id = fields.Many2one('library.rental', string="Rental", required=True, readonly=True)
    customer_id = fields.Many2one(string="Customer", related='rental_id.customer_id')
    book_id = fields.Many2one(string="Book", related='rental_id.book_id')