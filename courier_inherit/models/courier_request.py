# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CourierInherit(models.Model):
    _inherit = 'courier.request.lines'

    package_name_id = fields.Many2one('packaging.name', 'Package Name')
    dimensional_internal_id = fields.Many2one('dimension.internal', string='Dimensional Internal',
                                              related='package_name_id.dimensional_internal_id', readonly=False)
    dimensional_external_id = fields.Many2one('dimension.external', string='Dimensional External',
                                              related='package_name_id.dimensional_external_id', readonly=False)
    volume_weight = fields.Integer('Volumetric Weight', related='package_name_id.volume_weight', readonly=False)
    gross_weight = fields.Integer('Gross Weight', related='package_name_id.gross_weight', readonly=False)
    chargeable_weight = fields.Integer('Chargeable Weight', compute='compute_chargeable_weight')
    temperature = fields.Char('Temperature', related='package_name_id.temperature', readonly=False)

    def compute_chargeable_weight(self):
        for rec in self:
            if rec.volume_weight > rec.gross_weight:
                rec.chargeable_weight = rec.volume_weight
            else:
                rec.chargeable_weight = rec.gross_weight


class DevCourierRequest(models.Model):
    _inherit = 'dev.courier.request'

    account_no = fields.Char('Account No')
    purchase_order = fields.Char('Purchase Order')
    schedule_date = fields.Datetime('Scheduled pickup date')
    study_no = fields.Integer('Study No')
    service_terms = fields.Selection([
        ('door_to_door', 'Door to Door'),
        ('door_to_airport', 'Door to Airport'),
        ('airport_to_door', 'Airport to Door')
    ], string='Service Terms')
    inco_terms = fields.Char('Inco Terms')
    shipment_id = fields.Many2one('shipment.mode', 'Shipment Mode')
    dg_good = fields.Char('DG Good')
    dg_no = fields.Char('DG No')
    new_dg_goods = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),

    ], string='DG Goods')
    dg_number = fields.Char('DG No')
    collect_empty = fields.Char('Collect Empty Packaging')
    collect_data = fields.Char('Collect Data Logger')
    new_collect_empty = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Collect Empty Packaging')
    new_collect_data = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),
    ], string='Collect Data Logger')
    remarks = fields.Html(string='Remarks')
    customer_acc_no = fields.Char(string='Account No', related='sender_id.reference_no')
    dl_no = fields.Char(string='DL No.')
    account_id = fields.Many2one('res.partner', 'Account Name')
    account_street = fields.Char('Account Street', required="1")
    account_street2 = fields.Char('Account Street2')
    account_city = fields.Char('Account City', required="1")
    account_state_id = fields.Many2one('res.country.state', string='Account State', required="1")
    account_country_id = fields.Many2one('res.country', string='account Country', required="1")
    account_zip = fields.Char('Account Zip', required="1")
    contact_name = fields.Many2one('res.partner', 'Contact Name')
    contact_mobile = fields.Char('Contact Mobile', required="1", tracking=True)
    contact_email = fields.Char('Contact Email', required="1")
    shipper_contact_id = fields.Many2one('res.partner', 'Shipper Contact Name')
    consignee_contact_id = fields.Many2one('res.partner', 'Consignee Contact Name')

    # driver dispatched  in extra info page
    pickup_vender = fields.Many2one('res.partner', 'vendor Name')
    pickup_date = fields.Datetime('pickup date and time')
    person_name = fields.Char('Pickup Staff name(or) Employee Id')
    vehicle_number = fields.Char('vehicle Number')
    pickup_person_contact = fields.Integer("Pickup Staff Contact number")
    pickup_remark = fields.Char('Remarks')

    # parcel on board  in extra info page
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    pob_vehicle_number = fields.Char(string='Vehicle Number')
    pickup_datetime = fields.Datetime(string='Pickup Date & Time')
    pickup_temperature = fields.Float(string='Temperature at the time of Pickup(°F)')
    pob_remarks = fields.Text(string='Remarks')

    # Drop at airline  in extra info page
    drop_vender = fields.Many2one('res.partner', 'vendor Name')
    drop_date = fields.Datetime('Dropped at Airlines Date & Time')
    drop_vehicle_number = fields.Char('vehicle Number')
    drop_remark = fields.Text(string='Remarks')

    # Manifest(out) info  in extra info page
    mode_transport = fields.Selection([
        ('air', 'Air'),
        ('surface', 'Surface')
    ], string="Mode of Transport")
    airway_bill_number = fields.Char(string="Airway Bill Number")
    flight_number = fields.Char(string="Flight Number")
    from_country_id = fields.Many2one('res.country', string='From Country')
    from_location_id = fields.Many2one('res.country.state', string="From State")
    from_city = fields.Char('City')
    departure_status = fields.Datetime(string="Departure Status (Time & Date)")
    to_country_id = fields.Many2one('res.country', string='To Country')
    to_location_id = fields.Many2one('res.country.state', string="To Location")
    to_city = fields.Char('City')
    arrival_status = fields.Datetime(string="Arrival Status (Time & Date)")
    lr_number = fields.Char(string="LR Number (For Surface)")
    cd_number = fields.Char(string="CD Number")
    manifest_out_remarks = fields.Text(string="Remarks")
    via = fields.Char(string="Via")
    manifest_vendor_id = fields.Many2one('res.partner', 'Vendor')

    hide_flight_number_and_bill = fields.Boolean(compute="_compute_hide_fields", string="Hide Flight Number")
    hide_cd_lr_number = fields.Boolean(compute="_compute_hide_fields", string="Hide CD Number")

    # Manifest(in) info  in extra info page
    arrived_date = fields.Datetime('Arrived Date and Time')
    manifest_in_id = fields.Many2one('res.partner', 'Vendor')

    # Recovered info  in extra info page
    recovered_vendor_id = fields.Many2one('res.partner', 'Vendor Name')
    recovered_vehicle_number = fields.Char('vehicle Number')
    recovered_date = fields.Datetime('recovered Date and Time')
    recovered_remarks = fields.Text(string="Remarks")

    # Drs info  in extra info page
    drs_vendor_id = fields.Many2one('res.partner', 'Vendor Name')
    drs_date = fields.Datetime('DRS Date and Time')
    drs_name = fields.Char('Delivered By(Person Name or Employee id)')
    drs_vehicle_number = fields.Char('vehicle Number')
    drs_person_contact = fields.Char("Contact number")

    # Delivery info  in extra info page
    delivered_date = fields.Datetime('Date and Time')
    delivered_contact_det = fields.Char('contact details')
    receiver_number = fields.Char('Receiver Name')
    delivered_remarks = fields.Text(string="Remarks")

    # customer clearance info  in extra info page
    origin_name_id = fields.Many2one('res.partner', 'Vendor Name')
    origin_date = fields.Datetime('Date and Time')
    origin_remark = fields.Text(string='Remarks')

    # customer clearance at destination info  in extra info page
    destination_name_id = fields.Many2one('res.partner', 'Vendor Name')
    destination_date = fields.Datetime('Date and Time')
    duties_taxes = fields.Selection([
        ('paid_by_stc', 'Paid by STC'),
        ('paid_by_consignee', 'Paid by Consignee')
    ], string="Duties and Taxes")
    destination_remarks = fields.Text(string='Remarks')

    # shipment custom clearance info  in extra info page
    shipment_date = fields.Datetime('Date and Time')
    shipment_remarks = fields.Text(string='Remarks')

    # onhold info  in extra info page
    onhold_date = fields.Datetime('Date and Time')
    onhold_remarks = fields.Text(string='Remarks')

    # in transist info  in extra info page
    transit_date = fields.Datetime('Date and Time')
    transit_remarks = fields.Text(string='Remarks')

    # onhold info  in extra info page
    replenishment_date = fields.Datetime('Date and Time')
    dry_ice_wt = fields.Integer('Quantity in Kgs')
    replenishment_remarks = fields.Text(string='Remarks')

    # cancel info  in extra info page
    cancel_date = fields.Datetime('Date and Time')
    cancel_reason = fields.Selection([
        ('requested_by_customer', 'Requested by Customer'),
        ('shipment_cancelled', 'Shipment Cancelled')
    ], string="Reason for Cancellation")
    cancel_remarks = fields.Text(string='Remarks')

    # shipping field
    state_ids = fields.Many2many('dev.courier.stages', string='State Ids', compute='_compute_state_ids')
    state_id = fields.Many2one('dev.courier.stages', string='Status', index=True, tracking=True,
                               domain="[('id', 'in', state_ids)]")
    shipping_type_id = fields.Many2one('shipping.type', string="Shipping Type")

    invoices_line_ids = fields.One2many('courier.invoice.lines', 'courier_invoice_id', string='Invoce Lines')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id, readonly=True)
    amount_untaxed = fields.Monetary(string="Untaxed Amount", compute='_compute_amount_all', store=True)
    amount_tax = fields.Monetary(string="Taxes", compute='_compute_amount_all', store=True)
    amount_total = fields.Monetary(string="Total", compute='_compute_amount_all', store=True)

    show_drop_button = fields.Boolean(compute='_compute_show_buttons')
    show_drs_button = fields.Boolean(compute='_compute_show_buttons')
    show_manifest_button = fields.Boolean(compute='_compute_show_buttons')
    show_custom_clearance_button = fields.Boolean(compute='_compute_show_buttons')
    show_recovered_button = fields.Boolean(compute='_compute_show_buttons')
    show_shipping_clearance_button = fields.Boolean(compute='_compute_show_buttons')
    show_onhold_button = fields.Boolean(compute='_compute_show_buttons')

    # ___________________invoice details total___________

    @api.depends('invoices_line_ids.price_subtotal')
    def _compute_amount_all(self):
        for record in self:
            amount_untaxed = sum(line.product_qty * line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                                 for line in record.invoices_line_ids)
            amount_tax = sum(
                line.price_subtotal - (line.product_qty * line.price_unit * (1 - (line.discount or 0.0) / 100.0))
                for line in record.invoices_line_ids)
            record.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.depends('shipping_type_id')
    def _compute_state_ids(self):
        for rec in self:
            if rec.shipping_type_id:
                state_ids = self.env['dev.courier.stages'].search(
                    [('shipping_type_ids', 'in', rec.shipping_type_id.ids)])
                if state_ids:
                    rec.state_ids = state_ids.ids
                else:
                    rec.state_ids = False
            else:
                rec.state_ids = False

    # Method for changes of state one to another state based shipping type
    @api.depends('state_id', 'shipping_type_id')
    def _compute_show_buttons(self):
        for rec in self:
            rec.show_drop_button = False
            rec.show_drs_button = False
            rec.show_manifest_button = False
            rec.show_custom_clearance_button = False
            rec.show_recovered_button = False
            rec.show_shipping_clearance_button = False
            rec.show_onhold_button = False

            if rec.state_id.id == 3:
                # Drop Info button visible for Domestic, International Door To Port, International Door To Door
                if rec.shipping_type_id.id in [1, 3, 4]:
                    rec.show_drop_button = True

                # DRS Info button visible for Intercity
                if rec.shipping_type_id.id == 2:  # Replace with actual ID for Intercity
                    rec.show_drs_button = True

            elif rec.state_id.id == 4:
                # clearance Info button visible for  International Door To Port, International Door To Door
                if rec.shipping_type_id.id in [3, 4]:
                    rec.show_custom_clearance_button = True

                # manifest Info button visible for Intercity
                if rec.shipping_type_id.id == 1:  # Replace with actual ID for Intercity
                    rec.show_manifest_button = True
            elif rec.state_id.id == 5:
                if rec.shipping_type_id.id in [3, 4]:
                    rec.show_manifest_button = True
            elif rec.state_id.id == 7:
                if rec.shipping_type_id.id == 1:
                    # record airline Info button visible for domestic
                    rec.show_recovered_button = True
                if rec.shipping_type_id.id == 3:
                    # drs Info button visible for door to port
                    rec.show_drs_button = True
                if rec.shipping_type_id.id == 4:
                    # drs Info button visible for door to port
                    rec.show_shipping_clearance_button = True
            elif rec.state_id.id == 9:
                if rec.shipping_type_id.id == 4:
                    # recoverd Info button visible for door to door
                    rec.show_recovered_button = True
            elif rec.state_id.id == 10:
                if rec.shipping_type_id.id == 4:
                    # drs Info button visible for door to port
                    rec.show_drs_button = True

            elif rec.state_id.id == 13:
                if rec.shipping_type_id.id == 4:
                    # drs Info button visible for door to port
                    rec.show_onhold_button = True
            elif rec.state_id.id == 11:
                if rec.shipping_type_id.id == 1:
                    # drs Info button visible for door to port
                    rec.show_drs_button = True

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

    def get_service_terms_display(self):
        self.ensure_one()
        return dict(self.fields_get(allfields=['service_terms'])['service_terms']['selection']).get(self.service_terms)

    @api.onchange('account_id')
    def onchange_account_id(self):
        for rec in self:
            if rec.account_id:
                rec.account_street = rec.account_id.street
                rec.account_street2 = rec.account_id.street2
                rec.account_city = rec.account_id.city
                rec.account_state_id = rec.account_id.state_id.id
                rec.account_country_id = rec.account_id.country_id.id
                rec.account_zip = rec.account_id.zip

    def action_open_driverdispatch_popup(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.pickup.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_pob_popup(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.pob.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_drop_popup(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.drop.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_manifest_popup(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.manifest.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_arrived_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.arrived.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_recovered_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.recovered.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_drs_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.drs.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_delivered_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.delivered.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_origin_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.origin.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_destination_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.destination.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_shipment_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.shipment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_onhold_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.cleared.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_transit_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.transit.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_replenishment_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.replenishment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def action_open_cancel_popup(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'courier.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_courier_id': self.id,
            }
        }

    def _get_next_state(self, current_state, shipping_type):
        next_state = False
        if current_state and shipping_type:
            # Get the states filtered by the shipping type
            allowed_state_ids = self.env['dev.courier.stages'].search([
                ('shipping_type_ids', 'in', shipping_type.ids),
                ('sequence', '>', current_state.sequence)
            ])

            # Fetch the next state in sequence within the allowed states
            next_state = allowed_state_ids and allowed_state_ids.sorted('sequence')[0] or False
        return next_state

    @api.model
    def create_courier_customer_invoices(self):
        invoices = {}
        journal_id = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)

        # Retrieve active IDs from the context
        active_ids = self.env.context.get('active_ids', [])
        courier_records = self.env['dev.courier.request'].browse(active_ids)

        # Group courier requests by account (customer)
        courier_groups = {}
        for record in courier_records:
            account_id = record.account_id.id
            if account_id not in courier_groups:
                courier_groups[account_id] = []
            courier_groups[account_id].append(record.id)

        for record in self:
            account_id = record.account_id
            if not account_id:
                continue

            if account_id.id not in invoices:
                invoices[account_id.id] = {
                    'partner_id': account_id.id,
                    # 'courier_request_id': record.id,
                    'move_type': 'out_invoice',
                    'journal_id': journal_id.id if journal_id else False,
                    'currency_id': record.currency_id.id if record.currency_id else False,
                    'invoice_line_ids': [],
                    'state': 'draft',
                    'company_id': record.company_id.id if record.company_id else False,
                    'courier_ids': [(6, 0, courier_groups.get(account_id.id, []))],  # Add specific courier IDs
                    'is_consolidate_invoice': True,  # Mark as consolidated
                }

            invoices[account_id.id]['invoice_line_ids'].extend(record.get_courier_invoice_product_lines())

        created_invoices = []
        for invoice_vals in invoices.values():
            invoice = self.env['account.move'].create(invoice_vals)
            created_invoices.append(invoice)

        # Ensure an action is returned
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', 'in', [inv.id for inv in created_invoices])],
            'context': {'create': False},
        }

        #
        # action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        # action['domain'] = [('id', 'in', [inv.id for inv in created_invoices])]
        # return action

    def get_courier_invoice_product_lines(self):
        move_line_vals = []
        for line in self.invoices_line_ids:
            product_product = line.product_id.product_variant_id
            description = line.product_description if line.product_description else line.product_id.name
            move_line_vals.append((0, 0, {
                'product_id': product_product.id,
                'name': description,
                'quantity': line.product_qty,
                'product_uom_id': line.product_uom.id,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'tax_ids': [(6, 0, line.tax_id.ids)],
            }))
        return move_line_vals


class CourierInvoiceLines(models.Model):
    _name = 'courier.invoice.lines'

    courier_invoice_id = fields.Many2one('dev.courier.request', string='Invoice Request', ondelete='cascade')

    product_id = fields.Many2one('product.template', string="Product", required=True)
    product_description = fields.Char('Description')
    product_qty = fields.Float(string="Quantity", default=1.0)
    product_uom = fields.Many2one(comodel_name='uom.uom', string="Unit of Measure")
    tax_id = fields.Many2many(comodel_name='account.tax', string="Taxes")
    price_unit = fields.Float(string="Unit Price")
    discount = fields.Float(string="Discount (%)", default=0.0)
    price_subtotal = fields.Monetary(string="Subtotal", compute='_compute_price_subtotal', store=True)
    currency_id = fields.Many2one('res.currency', related='courier_invoice_id.currency_id', store=True, readonly=True)

    @api.depends('product_qty', 'price_unit', 'discount', 'tax_id')
    def _compute_price_subtotal(self):
        for line in self:
            subtotal = line.product_qty * line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            if line.tax_id:
                taxes = line.tax_id.compute_all(subtotal, currency=line.currency_id, quantity=1)
                line.price_subtotal = taxes['total_included']
            else:
                line.price_subtotal = subtotal
