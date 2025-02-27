from odoo import models, fields, api


class CourierInherit(models.TransientModel):

    _name = 'courier.manifest.wizard'

    mode_transport = fields.Selection([
        ('air', 'Air'),
        ('surface', 'Surface')
    ],string="Mode of Transport")
    airway_bill_number = fields.Char(string="Airway Bill Number")
    flight_number = fields.Char(string="Flight Number")
    from_country_id = fields.Many2one('res.country',string='From Country')
    from_location_id = fields.Many2one('res.country.state',string="From State")
    from_city = fields.Char('From City')
    departure_status = fields.Datetime(string="Departure Status (Time & Date)")
    to_country_id = fields.Many2one('res.country',string='To Country')
    to_location_id = fields.Many2one('res.country.state',string="To State")
    to_city = fields.Char('To City')
    arrival_status = fields.Datetime(string="Arrival Status (Time & Date)")
    
    lr_number = fields.Char(string="LR Number (For Surface)")
    cd_number = fields.Char(string="CD Number")

    remarks = fields.Text(string="Remarks")
    via = fields.Char(string="Via")
    courier_id = fields.Many2one('dev.courier.request')

    hide_flight_number_and_bill = fields.Boolean(compute="_compute_hide_fields", string="Hide Flight Number")
    hide_cd_lr_number = fields.Boolean(compute="_compute_hide_fields", string="Hide CD Number")
    manifest_vendor_id = fields.Many2one('res.partner','Vendor')

    #Hiding of manifest info fields
    @api.depends('mode_transport')
    def _compute_hide_fields(self):
        for record in self:
            if record.mode_transport == 'air':
                record.hide_flight_number_and_bill = True  
                record.hide_cd_lr_number = False
            elif record.mode_transport == 'surface':
                record.hide_flight_number_and_bill = False
                record.hide_cd_lr_number = True
            else:
                record.hide_flight_number_and_bill = False
                record.hide_cd_lr_number = False

    def action_move_to_manifest(self):
        self.ensure_one()
        courier_order = self.courier_id

        # Update the fields
        courier_order.write({
        'mode_transport': self.mode_transport,
        'airway_bill_number': self.airway_bill_number,
        'flight_number': self.flight_number,
        'from_country_id':self.from_country_id.id,
        'from_location_id': self.from_location_id.id,
        'from_city':self.from_city,
        'departure_status': self.departure_status,
        'to_country_id':self.to_country_id.id,
        'to_location_id': self.to_location_id.id,
        'to_city':self.to_city,
        'arrival_status': self.arrival_status,
        'lr_number': self.lr_number,
        'cd_number': self.cd_number,
        'manifest_out_remarks': self.remarks,
        'via': self.via,
        'manifest_vendor_id':self.manifest_vendor_id,
        })
        
        current_state = courier_order.state_id
        shipping_type = courier_order.shipping_type_id

        drop_state_id = 4
        manifest_out_state_id = 6  # Drop state ID (replace with the actual ID)
        clearance_state_id = 5   # DRS state ID (replace with the actual ID)

        if current_state.id == drop_state_id:
            if shipping_type.id == 1:  # Domestic, International Door To Port, International Door To Door
                # Move to "Drop" state
                # print("&&&&&&&&&&&&&&&&",shipping_type.id)
                next_state = self.env['dev.courier.stages'].browse(manifest_out_state_id)
            elif shipping_type.id in [3,4]:  # Intercity
                # Move to "DRS" state
                next_state = self.env['dev.courier.stages'].browse(clearance_state_id)
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


