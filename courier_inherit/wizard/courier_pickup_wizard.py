from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.pickup.wizard'


    pickup_vender = fields.Many2one('res.partner', 'vendor Name')
    pickup_date = fields.Datetime('pickup date and time')
    person_name = fields.Char('Pickup Staff name(or) Employee Id')
    vehicle_number = fields.Char('vehicle Number')
    pickup_person_contact = fields.Integer("Pickup Staff Contact number")
    remark = fields.Char('Remarks')
    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_pickup(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'pickup_vender': self.pickup_vender.id,
            'pickup_date': self.pickup_date,
            'person_name': self.person_name,
            'vehicle_number': self.vehicle_number,
            'pickup_person_contact': self.pickup_person_contact,
            'pickup_remark': self.remark,
        })

         # Update the state_id to the next state
        current_state = courier_order.state_id
        next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}


