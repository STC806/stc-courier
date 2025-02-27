from odoo import models, fields, api


class CourierPobWizard(models.TransientModel):
    _name = 'courier.pob.wizard'


    vendor_id = fields.Many2one('res.partner', string='Vendor')
    vehicle_number = fields.Char(string='Vehicle Number')
    pickup_datetime = fields.Datetime(string='Pickup Date & Time')
    pickup_temperature = fields.Float(string='Temperature at the time of Pickup')
    remarks = fields.Text(string='Remarks')
    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_pob(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'vendor_id': self.vendor_id.id,
            'pob_vehicle_number': self.vehicle_number,
            'pickup_datetime': self.pickup_datetime,
            'pickup_temperature': self.pickup_temperature,
            'pob_remarks': self.remarks,
        })

        # Update the state_id to the next state
        current_state = courier_order.state_id
        next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}
        

        # # Get current state and shipping type
        # current_state = courier_order.state_id
        # shipping_type = courier_order.shipping_type_id

        # # Custom logic to move to specific states based on shipping type and current state
        # if current_state.name == 'Parcel on Board (POB)':  # Make sure this matches the name of the POB state
        #     if shipping_type.name == 'Domestic' or shipping_type.name == 'International Door To Port' or shipping_type.name == 'International Door To Door':
        #         # Move to "Drop" state
        #         next_state = self.env['dev.courier.stages'].search([('name', '=', 'Drop')], limit=1)
        #     elif shipping_type.name == 'Intercity':
        #         # Move to "DRS" state
        #         next_state = self.env['dev.courier.stages'].search([('name', '=', 'DRS')], limit=1)
        #     else:
        #         # Default behavior if shipping type doesn't match the conditions
        #         next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        # else:
        #     # If current state is not POB, move to the next state in sequence
        #     next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)

        # # Update the state if a valid next state is found
        # if next_state:
        #     courier_order.state_id = next_state.id

        # return {'type': 'ir.actions.act_window_close'}

       