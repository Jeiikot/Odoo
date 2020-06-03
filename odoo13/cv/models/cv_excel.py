# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CvReportExcelWizard(models.TransientModel):
    _name = 'hr.employee.cv.report.wizard'


    employee_ref = fields.Many2one('hr.employee', invisible=1, copy=False, string="Employee")