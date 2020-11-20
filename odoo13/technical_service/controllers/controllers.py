# -*- coding: utf-8 -*-
# from odoo import http


# class TechnicalService(http.Controller):
#     @http.route('/technical_service/technical_service/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/technical_service/technical_service/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('technical_service.listing', {
#             'root': '/technical_service/technical_service',
#             'objects': http.request.env['technical_service.technical_service'].search([]),
#         })

#     @http.route('/technical_service/technical_service/objects/<model("technical_service.technical_service"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('technical_service.object', {
#             'object': obj
#         })
