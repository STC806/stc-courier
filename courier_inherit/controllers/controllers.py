# -*- coding: utf-8 -*-
# from odoo import http


# class CourierInherit(http.Controller):
#     @http.route('/courier_inherit/courier_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/courier_inherit/courier_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('courier_inherit.listing', {
#             'root': '/courier_inherit/courier_inherit',
#             'objects': http.request.env['courier_inherit.courier_inherit'].search([]),
#         })

#     @http.route('/courier_inherit/courier_inherit/objects/<model("courier_inherit.courier_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('courier_inherit.object', {
#             'object': obj
#         })

