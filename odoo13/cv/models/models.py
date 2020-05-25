# -*- coding: utf-8 -*-

import base64
from odoo import models, fields, api, _
from odoo.modules.module import get_module_resource

class CvAcademic(models.Model):
    _name = 'hr.employee.cv.academic'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    image_1920 = fields.Image(default=_default_image)
    certificate = fields.Selection([
        ('incomplete_bachelor', 'Bachiller Académico incompleto'),
        ('academic_bachelor', 'Bachiller Académico'),
        ('technical_bachelor', 'Bachiller Técnico'),
        ('graduate', 'Pregrado/Universitario'),
        ('specialization', 'Especialización'),
        ('master', 'Maestría'),
        ('doctorate', 'Doctorado'),
        ('post_doctorate', 'PostDoctorado'),
        ('other', 'Otro')
    ], 'Certificate Level', required=True, default='academic_bachelor', groups="hr.group_hr_user")
    state = fields.Selection([
        ('finished', 'Finished'),
        ('studying', 'Studying'),
        ('abandoned', 'Abandoned'),
    ], required=True, default="studying", groups="hr.group_hr_user")
    start_time = fields.Date("Start time", required=True, groups="hr.group_hr_user")
    end_time = fields.Date("End of time", groups="hr.group_hr_user", required=True,
                           states={'studying': [('required', False)]})
    study_field = fields.Char("Field of Study", required=True, groups="hr.group_hr_user")
    study_school = fields.Char("School", required=True, groups="hr.group_hr_user")
    cv_id = fields.Many2one('hr.employee.cv', invisible=1, copy=False, string="Empleado")

class Cv(models.Model):
    _name = 'hr.employee.cv'

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    name = fields.Char(string="Employee Name")
    image_1920 = fields.Image(default=_default_image)
    document_type = fields.Selection([
        ('cc', 'Cédula de ciudadanía'),
        ('ce', 'Cédula de extranjería'),
        ('passport', 'Pasaporte'),
        ('ti', 'Tarjeta de identidad'),
        ('rc', 'Registro civil'),
        ('pep', 'Permiso especial de permanencia'),
        ('other', 'Otro')], string="Document type", default='cc', groups="hr.group_hr_user")
    identification_id = fields.Char(string='Identification No', groups="hr.group_hr_user", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], groups="hr.group_hr_user", default="male", tracking=True)
    marital = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('cohabitant', 'Legal Cohabitant'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ], string='Marital Status', groups="hr.group_hr_user", default='single', tracking=True)
    country_id = fields.Many2one(
        'res.country', 'Nationality (Country)', groups="hr.group_hr_user", tracking=True)
    address_home = fields.Char(groups="hr.group_hr_user")
    mobile_phone = fields.Char(groups="hr.group_hr_user")
    email = fields.Char(groups="hr.group_hr_user")
    city = fields.Char(groups="hr.group_hr_user")
    place_of_birth = fields.Char('Place of Birth', groups="hr.group_hr_user", tracking=True)
    country_of_birth = fields.Many2one('res.country', string="Country of Birth", groups="hr.group_hr_user",
                                       tracking=True)
    birthday = fields.Date('Date of Birth', groups="hr.group_hr_user", tracking=True)
    job_id = fields.Many2one('hr.job', 'Job Position')
    job_title = fields.Char("Job Title")
    academic_line_ids = fields.One2many('hr.employee.cv.academic', 'cv_id')
    employee_ref = fields.Many2one('hr.employee', invisible=1, copy=False, string="Employee")

    @api.onchange('job_id')
    def _onchange_job_id(self):
        if self.job_id:
            self.job_title = self.job_id.name

    @api.onchange('employee_ref')
    def _onchange_employee_id(self):
        if self.employee_ref:
            self.job_id = self.employee_ref.job_id
            self.name = self.employee_ref.name
            self.image_1920 = self.employee_ref.image_1920
            self.identification_id = self.employee_ref.identification_id
            self.gender = self.employee_ref.gender
            self.marital = self.employee_ref.marital
            self.country_id = self.employee_ref.country_id
            self.place_of_birth = self.employee_ref.place_of_birth
            self.country_of_birth = self.employee_ref.country_of_birth
            self.birthday = self.employee_ref.birthday

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _cv_count(self):
        for each in self:
            cv_ids = self.env['hr.employee.cv'].search([('employee_ref', '=', each.id)])
            each.cv_count = len(cv_ids)

    """
    def cv_view(self):
        self.ensure_one()
        domain = [('employee_ref', '=', self.id)]

        vals = {
            'employee_ref': self.id,
            'name': self.name,
        }
        new_cv = self.env['hr.employee.cv'].create(vals)<
        context = dict(self.env.context)
        context['view_form_cv'] = 'edit'       
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'hr.employee.cv',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            #'res_id': new_cv.id,
            #'context': context
            'context': "{'default_employee_ref': %s, 'default_name': '%s'}" % (self.id, self.name)
        }"""

    cv_count = fields.Integer(compute='_cv_count', string='# Documents')
    cv_ids = fields.One2many('hr.employee.cv', 'employee_ref')