# -*- coding: utf-8 -*-

import base64
from io import BytesIO

from odoo import models, fields, api, _

import xlsxwriter

class CvReportExcelWizard(models.TransientModel):
    _name = 'hr.employee.cv.report.wizard'

    employee_ref = fields.Many2one('hr.employee', invisible=1, copy=False, string="Employee")

    def get_item_data(self):
        file_name = _('cv report.xlsx')
        fp = BytesIO()

        workbook = xlsxwriter.Workbook(fp)

        worksheet = workbook.add_worksheet('CV Report')

        worksheet.write(1, 1, 'test')

        workbook.close()
        file_download = base64.b64encode(fp.getvalue())
        fp.close()
        excel_context = self.with_context(default_name=file_name, default_file_download=file_download)

        return {
            'name': 'cv report Download',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.employee.cv.report.excel',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': excel_context._context,
        }


class CvReportExcel(models.TransientModel):
    _name = 'hr.employee.cv.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('Download payroll', readonly=True)