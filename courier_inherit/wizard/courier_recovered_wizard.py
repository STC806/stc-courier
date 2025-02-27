from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.recovered.wizard'

    recovered_vendor_id = fields.Many2one('res.partner','Vendor Name')
    vehicle_number = fields.Char('vehicle Number')
    recovered_date = fields.Datetime('recovered Date and Time')
    remarks = fields.Text(string="Remarks")

    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_recovered(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'recovered_date': self.recovered_date,
            'recovered_vehicle_number':self.vehicle_number,
            'recovered_vendor_id':self.recovered_vendor_id,
            'recovered_remarks':self.remarks,

        })
         
        # Get current state and shipping type
        current_state = courier_order.state_id
        shipping_type = courier_order.shipping_type_id

        manifest_in_state_id = 7  # Parcel on Board (POB) state ID
        ship_state_id = 8  # Drop state ID (replace with the actual ID)
        drs_state_id = 12   # DRS state ID (replace with the actual ID)
        recover_state_id = 10

        if current_state.id == manifest_in_state_id:
            if shipping_type.id == 1:  # Domestic, International Door To Port, International Door To Door
                # Move to "Drop" state
                next_state = self.env['dev.courier.stages'].browse(recover_state_id)
            elif shipping_type.id == 3:  # Intercity
                # Move to "DRS" state
                print("&&&&&&&&&&&&&&&&",shipping_type.id)
                next_state = self.env['dev.courier.stages'].browse(drs_state_id)
                print("^^^^^^^^^^",next_state)
            elif shipping_type.id == 4:
                next_state = self.env['dev.courier.stages'].browse(ship_state_id)
            else:
                # Default behavior if shipping type doesn't match the conditions
                next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)

        else:
            # If current state is not POB, move to the next state in sequence
            next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
            print("*****************",next_state)

        # Update the state if a valid next state is found
        if next_state:
            print("*****************1",next_state)
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'} 


        # # Update the state_id to the next state
        # current_state = courier_order.state_id
        # next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        # if next_state:
        #     courier_order.state_id = next_state.id

        # return {'type': 'ir.actions.act_window_close'}


