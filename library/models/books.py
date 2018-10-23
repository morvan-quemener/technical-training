# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class Books(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title')
    authors_ids = fields.Many2many('library.partner', string="Authors")
    edition_date =  fields.Date(string='Edition date',)
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    rental_ids = fields.One2many('library.rental', 'book_id', string='Rentals')
    

class BookCopy(models.Model):
    _name = 'library.bookcopy'
    _description = 'Book copy'    
    _inherits = {'library.book': 'book_id'}
    
    book_id = fields.Many2one('library.book', String="Book", ondelete="cascade", required=True)
    id_copy = fields.Char(String="ID copy", required=True)
    
    _sql_constraints = [('unicite_bookcopy', 'unique(id_copy)', 'Error, same ID copy for more than once book copy.')]
    
    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {}, id_copy=_('%s (copy)') % self.id_copy)
        return super(BookCopy, self).copy(default)

    
  