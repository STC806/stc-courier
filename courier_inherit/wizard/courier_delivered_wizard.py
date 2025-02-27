from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.delivered.wizard'

    delivered_date = fields.Datetime('delivered Date and Time')
    delivered_contact_det = fields.Char('contact details')
    receiver_number = fields.Char('Receiver Name')
    remarks = fields.Text(string="Remarks")

    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_delivered(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'delivered_date': self.delivered_date,
            'receiver_number':self.receiver_number,
            'delivered_remarks' :self.remarks

        })

        # Update the state_id to the next state
        current_state = courier_order.state_id
        next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}


