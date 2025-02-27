from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.origin.wizard'

    origin_name_id = fields.Many2one('res.partner', 'Vendor Name')
    origin_date = fields.Datetime('Date and Time')
    remark = fields.Text(string='Remarks')
    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_origin(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'origin_name_id': self.origin_name_id.id,
            'origin_date':self.origin_date,
            'origin_remark' :self.remark,

        })

        # Update the state_id to the next state
        current_state = courier_order.state_id
        next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}


