from odoo import models, fields, api

class ResBank(models.Model):
    _inherit = 'res.partner.bank'

    cheque_doc = fields.Binary('Cheque Doc')