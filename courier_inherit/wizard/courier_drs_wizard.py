from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.drs.wizard'

    drs_vendor_id = fields.Many2one('res.partner', 'Vendor Name')
    drs_date = fields.Datetime('DRS Date and Time')
    drs_name = fields.Char('Delivered By(Person Name or Employee id)')
    drs_vehicle_number = fields.Char('vehicle Number')
    drs_person_contact = fields.Char("Contact number")
    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_drs(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'drs_date': self.drs_date,
            'drs_name':self.drs_name,
            'drs_vendor_id':self.drs_vendor_id.id,
            'drs_vehicle_number':self.drs_vehicle_number,
            'drs_person_contact' : self.drs_person_contact,

        })
        
        # Get current state and shipping type
        current_state = courier_order.state_id
        shipping_type = courier_order.shipping_type_id

        pob_state_id = 3  # Parcel on Board (POB) state ID
        drop_state_id = 4  # Drop state ID (replace with the actual ID)
        drs_state_id = 12   # DRS state ID (replace with the actual ID)
        recover_state_id = 10
        manifest_in_state_id = 7

        if current_state.id == pob_state_id:
            if shipping_type.id in [1, 3, 4]:  # Domestic, International Door To Port, International Door To Door
                # Move to "Drop" state
                next_state = self.env['dev.courier.stages'].browse(drop_state_id)
            elif shipping_type.id == 2:  # Intercity
                # Move to "DRS" state
                print("&&&&&&&&&&&&&&&&",shipping_type.id)
                next_state = self.env['dev.courier.stages'].browse(drs_state_id)
                print("^^^^^^^^^^",next_state)
            else:
                # Default behavior if shipping type doesn't match the conditions
         
                next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        
        elif current_state.id == recover_state_id:
            if shipping_type.id == 4:
                next_state = self.env['dev.courier.stages'].browse(drs_state_id)
        elif current_state.id == manifest_in_state_id:
            if shipping_type.id == 3:
                next_state = self.env['dev.courier.stages'].browse(drs_state_id)

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


