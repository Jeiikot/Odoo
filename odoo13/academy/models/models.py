from odoo import models, fields, api

class Teachers(models.Model):
    _name = 'academy.teachers'

    name = fields.Char()
    biography = fields.Html()

    course_ids = fields.One2many('academy.courses', 'teacher_id', string="Courses")
    # category_course_ids = fields.One2many('academy.category_courses', 'teacher_id', string="Category Courses")

class Courses(models.Model):
    _name = 'academy.courses'
    _inherit = 'mail.thread'

    name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")

# class categoryCourses(models.Model):
#     _name = 'academy.category_courses'
#     _inherit = 'product.template'
#
#     name = fields.Char()
#     teacher_id = fields.Many2one('academy.teachers', string="Teacher")