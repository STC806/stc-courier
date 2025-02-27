from odoo import models, fields, api

class ShipmentMode(models.Model):

    _name = 'shipment.mode'
    _rec_name = 'shipment_name'

    shipment_name = fields.Char('Shipment Mode')