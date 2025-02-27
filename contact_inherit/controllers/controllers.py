# -*- coding: utf-8 -*-
# from odoo import http


# class ContactInherit(http.Controller):
#     @http.route('/contact_inherit/contact_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contact_inherit/contact_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contact_inherit.listing', {
#             'root': '/contact_inherit/contact_inherit',
#             'objects': http.request.env['contact_inherit.contact_inherit'].search([]),
#         })

#     @http.route('/contact_inherit/contact_inherit/objects/<model("contact_inherit.contact_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contact_inherit.object', {
#             'object': obj
#         })

