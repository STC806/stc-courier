from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.destination.wizard'

    destination_name_id = fields.Many2one('res.partner','Vendor Name')
    destination_date = fields.Datetime('Date and Time')
    duties_taxes = fields.Selection([
        ('paid_by_stc', 'Paid by STC'),
        ('paid_by_consignee', 'Paid by Consignee')
    ],string="Duties and Taxes")
    remarks = fields.Text(string='Remarks')

    courier_id = fields.Many2one('dev.courier.request')

    def action_move_to_destination(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
            'destination_name_id': self.destination_name_id.id,
            'destination_date':self.destination_date,
            'duties_taxes': self.duties_taxes,
            'destination_remarks':self.remarks,

        })

        # Update the state_id to the next state
        current_state = courier_order.state_id
        next_state = self.env['dev.courier.stages'].search([('sequence', '>', current_state.sequence)], limit=1)
        if next_state:
            courier_order.state_id = next_state.id

        return {'type': 'ir.actions.act_window_close'}


