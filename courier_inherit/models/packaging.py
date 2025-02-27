from odoo import models, fields, api

class Packaging(models.Model):
    _name = 'packaging.name'
    _rec_name = 'packaging_name'

    packaging_name = fields.Char('Packaging Name')
    dimensional_internal_id = fields.Many2one('dimension.internal',string='Dimensional Internal')
    dimensional_external_id = fields.Many2one('dimension.external',string='Dimensional External')
    volume_weight = fields.Integer('Volumetric Weight')
    gross_weight = fields.Integer('Gross Weight')
    temperature = fields.Char('Temperature')
