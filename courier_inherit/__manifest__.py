# -*- coding: utf-8 -*-
{
    'name': "courier_inherit",

    'summary': "Courier inherit",

    'description': """Courier inherit""",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'dev_courier_management','web','account'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/dimension_internal_views.xml',
        'views/packaging.xml',
        'views/dimension_external_view.xml',
        'views/courier_request.xml',
        'views/invoice_inherit.xml',
        'views/shipment_mode.xml',
        'wizard/courier_pickup_wizard.xml',
        'wizard/courier_drop_wizard.xml',
        'wizard/courier_manifest_wizard.xml',
        'wizard/courier_arrived_wizard.xml',
        'wizard/courier_recovered_wizard.xml',
        'wizard/courier_drs_wizard.xml',
        'wizard/courier_delivered_wizard.xml',
        'wizard/courier_clearance_origin_wizard.xml',
        'wizard/courier_clearance_destination_wizard.xml',
        'wizard/courier_shipment_wizard.xml',
        'wizard/courier_custom_cleared_wizard.xml',
        'wizard/courier_transit_wizard.xml',
        'wizard/courier_replenishment_wizard.xml',
        'wizard/courier_cancel_wizard.xml',
        'views/stages_view.xml',
        'views/shipment_type_views.xml',
        'wizard/courier_pob_wizard_view.xml',
        'views/courier_server.xml',
        'wizard/courier_request_wizard.xml',
        'wizard/cancel_request_wizard.xml',
        'report/invoice_report.xml',
        # 'wizard/consolidate_invoice.xml',
        'report/consolidate_invoice_report.xml',
        # 'views/stripped_layout_inherit.xml',
        # 'report/courier_report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
