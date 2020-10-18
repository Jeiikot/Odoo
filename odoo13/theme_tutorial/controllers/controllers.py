# -*- coding: utf-8 -*-
# from odoo import http


# class ThemeTutorial(http.Controller):
#     @http.route('/theme_tutorial/theme_tutorial/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/theme_tutorial/theme_tutorial/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('theme_tutorial.listing', {
#             'root': '/theme_tutorial/theme_tutorial',
#             'objects': http.request.env['theme_tutorial.theme_tutorial'].search([]),
#         })

#     @http.route('/theme_tutorial/theme_tutorial/objects/<model("theme_tutorial.theme_tutorial"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('theme_tutorial.object', {
#             'object': obj
#         })
