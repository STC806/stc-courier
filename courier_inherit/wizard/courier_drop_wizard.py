from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.drop.wizard'

    drop_vender = fields.Many2one('res.partner','Picked up in which vendor vehicle')
    drop_date = fields.Datetime('Dropped date and time')
    vehicle_number = fields.Char('vehicle Number')
    remark = fields.Text(string='Remarks')
    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_drop(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'drop_vender': self.drop_vender.id,
            'drop_date': self.drop_date,
            'drop_vehicle_number': self.vehicle_number,
            'drop_remark' : self.remark,
        })
        
        # Get current state and shipping type
        current_state = courier_order.state_id
        shipping_type = courier_order.shipping_type_id

        pob_state_id = 17  # Parcel on Board (POB) state ID
        drop_state_id = 3  # Drop state ID (replace with the actual ID)
        drs_state_id = 12   # DRS state ID (replace with the actual ID)

        if current_state.id == pob_state_id:
            if shipping_type.id in [1, 3, 4]:  # Domestic, International Door To Port, International Door To Door
                # Move to "Drop" state
                print("&&&&&&&&&&&&&&&&",shipping_type.id)
                next_state = self.env['dev.courier.stages'].browse(drop_state_id)
            elif shipping_type.id == 2:  # Intercity
                # Move to "DRS" state
                next_state = self.env['dev.courier.stages'].browse(drs_state_id)
            else:
                # Default behavior if shipping type doesn't match the conditions
                next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        else:
            # If current state is not POB, move to the next state in sequence
            next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)

        # Update the state if a valid next state is found
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}



        # # Update the state_id to the next state
        # current_state = courier_order.state_id
        # next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        # if next_state:
        #     courier_order.state_id = next_state.id

        # return {'type': 'ir.actions.act_window_close'}


