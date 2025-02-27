# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ContactInherit(models.Model):
    _inherit = 'res.partner'

    tan_no = fields.Char('Tan No.')
    tan_binary = fields.Binary('Tan No Document')
    iec_no = fields.Char('IEC No.')
    iec_binary = fields.Binary('IEC No Document')
    gst_binary = fields.Binary('GST Document')
    reference_no = fields.Char(string='Order Reference', required=True,
                               readonly=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'res.partner') or _('New')
        res = super(ContactInherit, self).create(vals)
        print(res.reference_no)
        return res



