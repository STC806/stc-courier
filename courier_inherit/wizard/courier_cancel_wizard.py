from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.cancel.wizard'

    cancel_date = fields.Datetime('Date and Time')
    cancel_reason = fields.Selection([
        ('requested_by_customer', 'Requested by Customer'),
        ('shipment_cancelled', 'Shipment Cancelled')
    ],string="Reason for Cancellation")
    remarks = fields.Text(string='Remarks')

    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_cancel(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'cancel_date':self.cancel_date,
            'cancel_reason':self.cancel_reason,
            'cancel_remarks':self.remarks,

        })

        # Update the state_id to the next state
        current_state = courier_order.state_id
        next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}


