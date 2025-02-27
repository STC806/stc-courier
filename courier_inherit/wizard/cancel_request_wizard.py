from odoo import models, fields, api

class CancelRequestWizard(models.TransientModel):
    _name = 'cancel.request.wizard'
    _description = 'Cancel Request Wizard'

    state_id = fields.Many2one('dev.courier.stages', string="State", readonly=True, default=lambda self: self._get_default_state())
    cancel_date = fields.Datetime(string='Date and Time')
    cancel_reason = fields.Selection([
        ('requested_by_customer', 'Requested by Customer'),
        ('shipment_cancelled', 'Shipment Cancelled')
    ], string="Reason for Cancellation", required=True)
    cancel_remarks = fields.Text(string='Remarks')

    @api.model
    def _get_default_state(self):
        # Search for the record in 'dev.courier.stages' with sequence=16
        return self.env['dev.courier.stages'].search([('sequence', '=', 16)], limit=1)

    def action_apply(self):
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            records = self.env['dev.courier.request'].browse(active_ids)
            records.write({
                'state_id': self.state_id.id,
                'cancel_date': self.cancel_date,
                'cancel_reason': self.cancel_reason,
                'cancel_remarks': self.cancel_remarks,
            })
