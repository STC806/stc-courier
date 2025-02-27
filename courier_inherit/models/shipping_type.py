from odoo import models, fields, api

class ShippingType(models.Model):
    _name = 'shipping.type'


    name = fields.Char(string='name')
    shipping_type = fields.Selection([
    ('domestic', 'Domestic'),
    ('intercity', 'Intercity'),
    ('international_door_to_port', 'International Door To Port'),
    ('international_door_to_door', 'International Door To Door')], string='Shipping Type')
    sequence = fields.Integer('Sequence')