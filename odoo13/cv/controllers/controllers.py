# -*- coding: utf-8 -*-
# from odoo import http


# class Cv(http.Controller):
#     @http.route('/cv/cv/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cv/cv/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cv.listing', {
#             'root': '/cv/cv',
#             'objects': http.request.env['cv.cv'].search([]),
#         })

#     @http.route('/cv/cv/objects/<model("cv.cv"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cv.object', {
#             'object': obj
#         })
