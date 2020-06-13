# -*- coding: utf-8 -*-

from datetime import datetime

import base64
from io import BytesIO

from odoo import models, fields, api, _

import xlsxwriter

class CvReportExcelWizard(models.TransientModel):
    _name = 'hr.employee.cv.report.wizard'

    employee_ref = fields.Many2one('hr.employee', invisible=1, copy=False, string="Employee")

    def get_excel(self):
        file_name = _('cv report.xlsx')
        fp = BytesIO()

        workbook = xlsxwriter.Workbook(fp)

        self.get_data(workbook)

        workbook.close()
        file_download = base64.b64encode(fp.getvalue())
        fp.close()
        # Two Alternative
        #excel_context = self.with_context(default_name=file_name, default_file_download=file_download)
        # 'context': excel_context._context,
        dict_context = {'default_name': file_name, 'default_file_download': file_download}

        return {
            'name': 'cv report Download',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.employee.cv.report.excel',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': dict_context,
        }

    def get_data(self, workbook):
        worksheet = workbook.add_worksheet('CV Report')
        # Template format
        heading_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'bold': True, 'size': 14})
        cell_text_format_1 = workbook.add_format({'align': 'center',
                                                  'bold': True, 'size': 9,
                                                  })
        cell_text_format_2 = workbook.add_format({'align': 'center',
                                                  'bold': False, 'size': 9,
                                                  })
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 20)
        worksheet.set_column('K:K', 20)
        worksheet.set_column('L:L', 20)
        worksheet.set_column('M:M', 20)
        worksheet.set_column('N:N', 20)

        # Write

        today = datetime.today()
        worksheet.merge_range('A1:F2', 'Curriculum Vitae', heading_format)
        worksheet.write('F3', "%s %s %s" % (today.day, today.strftime("%B"), today.year), cell_text_format_1)

        cv_lines = self.env['hr.employee.cv'].search([('employee_ref.id', '=', self.employee_ref.id)])
        cols = 0
        for line in cv_lines:
            worksheet.write(6, 0, "Employee", cell_text_format_1)
            worksheet.write(6, 1, "Nationality", cell_text_format_1)
            worksheet.write(6, 2, "Document Type", cell_text_format_1)
            worksheet.write(6, 3, "No.", cell_text_format_1)
            worksheet.write(6, 4,  "Gender", cell_text_format_1)
            worksheet.write(6, 5,  "Job Position", cell_text_format_1)
            worksheet.write(6, 6,  "Email", cell_text_format_1)
            worksheet.write(6, 7,  "Mobile Phone", cell_text_format_1)
            worksheet.write(6, 8, "Field of Study", cell_text_format_1)
            worksheet.write(6, 9, "School", cell_text_format_1)
            worksheet.write(6, 10, "State", cell_text_format_1)

            worksheet.write(7, 0 + cols, "%s" % line.name if line.name!=False else '', cell_text_format_2)
            worksheet.write(7, 1 + cols, "%s" % line.country_id.name if line.country_id!=False else '', cell_text_format_2)
            worksheet.write(7, 2 + cols, "%s" % line.document_type if line.document_type!=False else '', cell_text_format_2)
            worksheet.write(7, 3 + cols, "%s" % line.identification_id if line.identification_id!=False else '', cell_text_format_2)
            worksheet.write(7, 4 + cols, "%s" % line.gender if line.gender!=False else '', cell_text_format_2)
            worksheet.write(7, 5 + cols, "%s" % line.job_id.name if line.job_id.name!=False else '', cell_text_format_2)
            worksheet.write(7, 6 + cols, "%s" % line.email if line.email!=False else '', cell_text_format_2)
            worksheet.write(7, 7 + cols, "%s" % line.mobile_phone if line.mobile_phone!=False else '', cell_text_format_2)
            if line.academic_line_ids != None:
                study_field, study_school, state = str(), str(), str()
                for academic_line in line.academic_line_ids:
                    study_field += "%s \n" % academic_line.study_field
                    study_school += "%s \n" % academic_line.study_school
                    state += "%s \n" % academic_line.state
                worksheet.write(7, 8 + cols, "%s" % study_field if study_field != None else "", cell_text_format_2)
                worksheet.write(7, 9 + cols, "%s" % study_school if study_school != None else "", cell_text_format_2)
                worksheet.write(7, 10 + cols, "%s" % state if state != None else "", cell_text_format_2)
            else:
                cols += 1









class CvReportExcel(models.TransientModel):
    _name = 'hr.employee.cv.report.excel'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('Download payroll', readonly=True)