from odoo import models, fields, api

class DimensionInternal(models.Model):
    _name = 'dimension.internal'

    name = fields.Char("Dimensions Cm's internal")


class DimensionExternal(models.Model):
    _name = 'dimension.external'

    name = fields.Char("Dimensions Cm's External")

