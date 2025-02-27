from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class InvoiceInherit(models.Model):
    _inherit = 'account.move'

    courier_ids = fields.Many2many('dev.courier.request')
    is_consolidate_invoice = fields.Boolean()
    courier_request_count = fields.Integer(string="Sample Request Count", compute="_compute_courier_request_count")

    def action_view_courier_request(self):
        return {
            'name': _('Courier Request'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'dev.courier.request',
            'domain': [('id', 'in', self.courier_ids.ids)],
            'views_id': False,

        }

    def _compute_courier_request_count(self):
        for rec in self:
            rec.courier_request_count = len(rec.courier_ids)

    def _get_report_base_filename(self):
        if self.is_consolidate_invoice:
            raise ValidationError(_("This is a consolidated invoice. Please print the consolidated report instead."))
        return super(InvoiceInherit, self)._get_report_base_filename()

    # product_description = fields.Char('Description')
