# -*- coding: utf-8 -*-

from odoo import models, fields, api


class technicalServiceStage(models.Model):
    """ Model for case stages. This models the main stages of a Technical Service Request management flow. """

    _name = 'technical_service.stage'
    _description = 'Technical Service Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    done = fields.Boolean('Request Done')

class technicalServiceRequest(models.Model):
    _name = 'technical_service.request'

    _description = 'Technical Service Request'

    @api.returns('self')
    def _default_stage(self):
        return self.env['technical_service.stage'].search([], limit=1)

    name = fields.Char('Name', required=True, translate=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    description = fields.Text('Description')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    request_date = fields.Date('Request Date', tracking=True, default=fields.Date.context_today,
                               help="Date requested for the technical service to happen")
    stage_id = fields.Many2one('technical_service.stage', string='Stage', ondelete='restrict',
                               tracking=True, default=_default_stage, copy=False)

