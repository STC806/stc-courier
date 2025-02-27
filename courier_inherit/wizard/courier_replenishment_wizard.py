from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.replenishment.wizard'

    replenishment_date = fields.Datetime('Date and Time')
    dry_ice_wt = fields.Integer('Quantity in Kgs')
    remarks = fields.Text(string='Remarks')
    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_replenishment(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'replenishment_date':self.replenishment_date,
            'dry_ice_wt':self.dry_ice_wt,
            'replenishment_remarks':self.remarks

        })

        # Update the state_id to the next state
        current_state = courier_order.state_id
        next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}


