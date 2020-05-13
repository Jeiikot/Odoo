# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CV(models.Model):
    _name = 'hr.employee.cv'

    name = fields.Char()

    employee_ref = fields.Many2one('hr.employee', invisible=1, copy=False, string="Empleado")

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