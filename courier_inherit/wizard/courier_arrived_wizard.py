from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.arrived.wizard'

    arrived_date = fields.Datetime('Arrived Date and Time')
    manifest_in_id = fields.Many2one('res.partner','Vendor')
    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_arrived(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'arrived_date': self.arrived_date,
            'manifest_in_id':self.manifest_in_id.id,

        })
        
        # Update the state_id to the next state
        current_state = courier_order.state_id
        next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}


