# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning

class HrEmployeeDocument(models.Model):
    _name = 'hr.employee.cv.document'
    _description = 'Cv Documents'

    name = fields.Char('Document Name', required=True, copy=False)
    description = fields.Text(string='Description', copy=False)
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_rel', 'doc_id', 'attach_id3', string="Attachment",
                                         help='You can attach the copy of your document', copy=False)
    document_type = fields.Selection([
        ('cv', 'Curriculum vitae'),
        ('id', 'Identification document'),
        ('jc', 'Job certificate'),
        ('sc', 'Study certificate'),
        ('other', 'Other')],
        default="cv", string='Document Type', required=True)
    cv_ref = fields.Many2one('hr.employee.cv', invisible=True, copy=False)

class Cv(models.Model):
    _inherit = 'hr.employee.cv'

    def _document_count(self):
        for each in self:
            document_ids = self.env['hr.employee.cv.document'].search([('cv_ref', '=', each.id)])
            each.document_count = len(document_ids)

    def document_view(self):
        self.ensure_one()
        domain = [
            ('cv_ref', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'hr.employee.cv.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_cv_ref': '%s'}" % self.id
        }

    document_count = fields.Integer(compute='_document_count', string='# Documents')

class CvAttachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel = fields.Many2many('hr.employee.cv.document', 'doc_attachment_id', 'attach_id3', 'doc_id',
                                      string="Attachment", invisible=True)