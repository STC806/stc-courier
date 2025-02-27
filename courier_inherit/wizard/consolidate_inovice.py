from odoo import models, fields, api

class InvoiceReportWizard(models.TransientModel):
    _name = 'invoice.report.wizard'
    _description = 'Invoice Report Wizard'

    selection_type = fields.Selection([
        ('by_date', 'By Date'),
        ('by_invoice', 'By Invoice')
    ], string='Selection Type', required=True, default='by_date')

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    invoice_ids = fields.Many2many('account.move', string='Invoices', domain=[('move_type', '=', 'out_invoice')])
    customer_id = fields.Many2one('res.partner', string='Customer')

    # def generate_invoice_report(self):
    #     if self.selection_type == 'by_date':
    #         # Get invoices within the date range
    #         domain = [
    #             ('move_type', '=', 'out_invoice'),
    #             ('invoice_date', '>=', self.from_date),
    #             ('invoice_date', '<=', self.to_date)
    #         ]
    #         if self.customer_id:
    #             domain.append(('partner_id', '=', self.customer_id.id))
    #
    #         invoices = self.env['account.move'].search(domain)
    #
    #     elif self.selection_type == 'by_invoice':
    #         invoices = self.invoice_ids
    #
    #     # Return the action to print the report
    #     return self.env.ref('courier_inherit.invoice_report_action').report_action(
    #         self, data={'invoice_ids': invoices.ids}
    #     )


# class ReportInvoice(models.AbstractModel):
#     _name = 'report.courier_inherit.report_monthly_invoice'
#
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         invoice_ids = data.get('invoice_ids', [])
#         docs = self.env['account.move'].browse(invoice_ids)
#         return {
#             'doc_ids': invoice_ids,
#             'doc_model': 'account.move',
#             'docs': docs,
#         }

