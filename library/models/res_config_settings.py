# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

#from ast import literal_eval

from odoo import api, fields, models
#from odoo.exceptions import AccessDenied


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    daily_price = fields.Float(string="Daily price", required=True)
    fine_price = fields.Float(string="Fine price", required=True)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            daily_price=float(get_param('library.daily_price')),
            fine_price=float(get_param('library.fine_price'))
        )
        return res

    def set_values(self):
        #if not self.user_has_groups('website.group_website_designer'):
        #    raise AccessDenied()
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('library.daily_price', self.daily_price)
        set_param('library.fine_price', self.fine_price)
