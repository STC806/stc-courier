from odoo import models, fields, api
from odoo.exceptions import UserError


class CourierRequestWizard(models.TransientModel):
    _name = 'courier.request.wizard'
    # _description = 'Courier Request Wizard for State Transition'

    next_state_id = fields.Many2one('dev.courier.stages', string="Next State", readonly=True)
    shipping_type_id = fields.Many2one('shipping.type')


    # pickup
    pickup_vender = fields.Many2one('res.partner', 'vendor Name')
    pickup_date = fields.Datetime('pickup date and time')
    person_name = fields.Char('Pickup Staff name(or) Employee Id')
    pickup_vehicle_number = fields.Char('vehicle Number')
    pickup_person_contact = fields.Integer("Pickup Staff Contact number")
    pickup_remark = fields.Char('Remarks')

    #pob
    pob_vendor_id = fields.Many2one('res.partner', string='Vendor')
    pob_vehicle_number = fields.Char(string='Vehicle Number')
    pob_pickup_datetime = fields.Datetime(string='Pickup Date & Time')
    pob_pickup_temperature = fields.Float(string='Temperature at the time of Pickup')
    pob_remarks = fields.Text(string='Remarks')


    # mainfest(in) arrived wizard
    arrived_date = fields.Datetime('Arrived Date and Time')
    manifest_in_id = fields.Many2one('res.partner', 'Vendor')
    courier_id = fields.Many2one('dev.courier.request')

    # cancel wizard
    cancel_date = fields.Datetime('Date and Time')
    cancel_reason = fields.Selection([
        ('requested_by_customer', 'Requested by Customer'),
        ('shipment_cancelled', 'Shipment Cancelled')
    ], string="Reason for Cancellation")
    cancel_remarks = fields.Text(string='Remarks')

    # clearance destination
    destination_name_id = fields.Many2one('res.partner', 'Vendor Name')
    destination_date = fields.Datetime('Date and Time')
    duties_taxes = fields.Selection([
        ('paid_by_stc', 'Paid by STC'),
        ('paid_by_consignee', 'Paid by Consignee')
    ], string="Duties and Taxes")
    clear_dest_remarks = fields.Text(string='Remarks')

    # clearance origin
    origin_name_id = fields.Many2one('res.partner', 'Vendor Name')
    origin_date = fields.Datetime('Date and Time')
    origin_clear_remark = fields.Text(string='Remarks')

    # custom clearance
    onhold_date = fields.Datetime('Date and Time')
    custom_clear_remarks = fields.Text(string='Remarks')

    # delivered wizard
    delivered_date = fields.Datetime('delivered Date and Time')
    delivered_contact_det = fields.Char('contact details')
    receiver_number = fields.Char('Receiver Name')
    delivered_remarks = fields.Text(string="Remarks")

    # drop wizard
    drop_vender = fields.Many2one('res.partner', 'Picked up in which vendor vehicle')
    drop_date = fields.Datetime('Dropped date and time')
    drop_vehicle_number = fields.Char('vehicle Number')
    drop_remark = fields.Text(string='Remarks')

    # drs wizard
    drs_vendor_id = fields.Many2one('res.partner', 'Vendor Name')
    drs_date = fields.Datetime('DRS Date and Time')
    drs_name = fields.Char('Delivered By(Person Name or Employee id)')
    drs_vehicle_number = fields.Char('vehicle Number')
    drs_person_contact = fields.Char("Contact number")

    # manifest
    mode_transport = fields.Selection([
        ('air', 'Air'),
        ('surface', 'Surface')
    ], string="Mode of Transport")
    airway_bill_number = fields.Char(string="Airway Bill Number")
    flight_number = fields.Char(string="Flight Number")
    from_country_id = fields.Many2one('res.country', string='From Country')
    from_location_id = fields.Many2one('res.country.state', string="From State")
    from_city = fields.Char('From City')
    departure_status = fields.Datetime(string="Departure Status (Time & Date)")
    to_country_id = fields.Many2one('res.country', string='To Country')
    to_location_id = fields.Many2one('res.country.state', string="To State")
    to_city = fields.Char('To City')
    arrival_status = fields.Datetime(string="Arrival Status (Time & Date)")

    lr_number = fields.Char(string="LR Number (For Surface)")
    cd_number = fields.Char(string="CD Number")

    remarks = fields.Text(string="Remarks")
    via = fields.Char(string="Via")

    hide_flight_number_and_bill = fields.Boolean(compute="_compute_hide_fields", string="Hide Flight Number")
    hide_cd_lr_number = fields.Boolean(compute="_compute_hide_fields", string="Hide CD Number")
    manifest_vendor_id = fields.Many2one('res.partner', 'Vendor')



    # recovered
    recovered_vendor_id = fields.Many2one('res.partner', 'Vendor Name')
    recovered_vehicle_number = fields.Char('vehicle Number')
    recovered_date = fields.Datetime('recovered Date and Time')
    recovered_remarks = fields.Text(string="Remarks")

    # replenishment
    replenishment_date = fields.Datetime('Date and Time')
    dry_ice_wt = fields.Integer('Quantity in Kgs')
    replenishment_remarks = fields.Text(string='Remarks')

    # shipment
    shipment_date = fields.Datetime('Date and Time')
    shipment_remarks = fields.Text(string='Remarks')

    # transit
    transit_date = fields.Datetime('Date and Time')
    transit_remarks = fields.Text(string='Remarks')

    show_driver_dispatch = fields.Boolean()
    show_pob = fields.Boolean()
    show_drop_airlines = fields.Boolean()
    show_custom_clearance = fields.Boolean()
    show_manifest_out = fields.Boolean()
    show_manifest_in = fields.Boolean()
    show_shipment_custom = fields.Boolean()
    show_clear_destination = fields.Boolean()
    show_recovered_airlines = fields.Boolean()
    show_dre_ice_replenishment = fields.Boolean()
    show_delivery_run_sheet = fields.Boolean()
    show_delivered = fields.Boolean()
    show_onhold = fields.Boolean()
    show_in_transit = fields.Boolean()


    # Hiding of manifest info fields
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

    @api.model
    def default_get(self, fields_list):
        res = super(CourierRequestWizard, self).default_get(fields_list)
        active_ids = self.env.context.get('active_ids')

        if active_ids:
            records = self.env['dev.courier.request'].browse(active_ids)
            if records and all(
                    r.state_id == records[0].state_id and r.shipping_type_id == records[0].shipping_type_id
                    for r in records
            ):
                shipping_id = records[0].shipping_type_id.id


                # Retrieve the next state and set it to `next_state_id`
                next_state = self.env['dev.courier.request']._get_next_state(
                    records[0].state_id, records[0].shipping_type_id
                )
                if next_state:
                    res['next_state_id'] = next_state.id
                    res['shipping_type_id'] = shipping_id

                    # Set show_pickup_vender based on next_state_id.sequence
                    res['show_driver_dispatch'] = next_state.sequence == 2
                    res['show_pob'] = next_state.sequence == 3
                    if next_state.sequence == 4 and records[0].shipping_type_id.sequence != 2:
                        res['show_drop_airlines'] = True

                    if next_state.sequence == 5 and records[0].shipping_type_id.sequence not in (1, 2):
                        res['show_custom_clearance'] = True

                    if next_state.sequence == 6 and records[0].shipping_type_id.sequence != 2:
                        res['show_manifest_out'] = True

                    if next_state.sequence == 7 and records[0].shipping_type_id.sequence != 2:
                        res['show_manifest_in'] = True

                    if next_state.sequence == 8 and records[0].shipping_type_id.sequence == 4:
                        res['show_shipment_custom'] = True

                    if next_state.sequence == 9 and records[0].shipping_type_id.sequence == 4:
                        res['show_clear_destination'] = True

                    if next_state.sequence == 10 and records[0].shipping_type_id.sequence in (1,4):
                        res['show_recovered_airlines'] = True

                    if next_state.sequence == 11 and records[0].shipping_type_id.sequence == 1:
                        res['show_dre_ice_replenishment'] = True

                    if next_state.sequence == 12:
                        res['show_delivery_run_sheet'] = True

                    if next_state.sequence == 13:
                        res['show_delivered'] = True

                    if next_state.sequence == 14 and records[0].shipping_type_id.sequence == 4:
                        res['show_onhold'] = True

                    if next_state.sequence == 15 and records[0].shipping_type_id.sequence == 4:
                        res['show_in_transit'] = True


                else:
                    raise UserError("No next state found for the selected records.")
            else:
                raise UserError("Please select records with the same state and shipping type.")

        return res

    def confirm_action(self):
        active_ids = self.env.context.get('active_ids')
        records = self.env['dev.courier.request'].browse(active_ids)

        # Collect fields based on visibility
        visible_fields = {}
        if self.show_driver_dispatch:
            visible_fields.update({
                'pickup_vender': self.pickup_vender,
                'pickup_date': self.pickup_date,
                'person_name': self.person_name,
                'vehicle_number': self.pickup_vehicle_number,
                'pickup_person_contact': self.pickup_person_contact,
                'pickup_remark': self.pickup_remark,
            })
        if self.show_pob:
            visible_fields.update({
                'vendor_id': self.pob_vendor_id.id,
                'pob_vehicle_number': self.pob_vehicle_number,
                'pickup_datetime': self.pob_pickup_datetime,
                'pickup_temperature': self.pob_pickup_temperature,
                'pob_remarks': self.pob_remarks,
            })
        if self.show_drop_airlines:
            visible_fields.update({
                'drop_vender': self.drop_vender.id,
                'drop_date': self.drop_date,
                'drop_vehicle_number': self.drop_vehicle_number,
                'drop_remark': self.drop_remark,
            })
        if self.show_custom_clearance:
            visible_fields.update({
                'origin_name_id': self.origin_name_id.id,
                'origin_date': self.origin_date,
                'origin_remark': self.origin_clear_remark,
            })

        if self.show_manifest_out:
            visible_fields.update({
                'mode_transport': self.mode_transport,
                'manifest_vendor_id': self.manifest_vendor_id.id,
                'origin_remark': self.origin_clear_remark,
                'airway_bill_number':self.airway_bill_number,
                'flight_number':self.flight_number,
                'from_country_id':self.from_country_id.id,
                'from_location_id':self.from_location_id.id,
                'from_city':self.from_city,
                'departure_status':self.departure_status,
                'to_country_id':self.to_country_id.id,
                'to_location_id':self.to_location_id.id,
                'to_city':self.to_city,
                'arrival_status':self.arrival_status,
                'lr_number':self.lr_number,
                'cd_number':self.cd_number,
                'manifest_out_remarks':self.remarks,

            })

        if self.show_manifest_in:
            visible_fields.update({
                'arrived_date': self.arrived_date,
                'manifest_in_id': self.manifest_in_id.id,


            })

        if self.show_shipment_custom:
            visible_fields.update({
                'shipment_date': self.shipment_date,
                'shipment_remarks': self.shipment_remarks,


            })

        if self.show_clear_destination:
            visible_fields.update({
                'destination_name_id': self.destination_name_id.id,
                'destination_date': self.destination_date,
                'duties_taxes': self.duties_taxes,
                'clear_dest_remarks': self.clear_dest_remarks,


            })


        if self.show_recovered_airlines:
            visible_fields.update({
                'recovered_vendor_id': self.recovered_vendor_id.id,
                'recovered_vehicle_number': self.recovered_vehicle_number,
                'recovered_date': self.recovered_date,
                'recovered_remarks': self.recovered_remarks,


            })

        if self.show_dre_ice_replenishment:
            visible_fields.update({
                'drs_vendor_id': self.drs_vendor_id.id,
                'drs_date': self.drs_date,
                'drs_name': self.drs_name,
                'drs_vehicle_number': self.drs_vehicle_number,
                'drs_person_contact': self.drs_person_contact,


            })


        if self.show_dre_ice_replenishment:
            visible_fields.update({
                'replenishment_date': self.replenishment_date,
                'dry_ice_wt': self.dry_ice_wt,
                'replenishment_remarks': self.replenishment_remarks,

            })

        if self.show_delivered:
            visible_fields.update({
                'delivered_date': self.delivered_date,
                'receiver_number': self.receiver_number,
                'delivered_remarks': self.delivered_remarks,

            })

        if self.show_onhold:
            visible_fields.update({
                'onhold_date': self.onhold_date,
                'onhold_remarks': self.custom_clear_remarks,

            })

        if self.show_in_transit:
            visible_fields.update({
                'transit_date': self.transit_date,
                'transit_remarks': self.transit_remarks,

            })


        visible_fields.update({'state_id': self.next_state_id.id})

        for record in records:
            record.write(visible_fields)
