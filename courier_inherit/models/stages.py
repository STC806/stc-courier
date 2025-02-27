from odoo import models, fields, api

class courier_stages(models.Model):
    _inherit = 'dev.courier.stages'

    stages_type = fields.Many2many('shipment.mode', string='Shipping Types')
    shipping_type_ids = fields.Many2many('shipping.type', string='Shipping Types')
