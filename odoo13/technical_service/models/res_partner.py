# -*- coding: utf-8 -*-
from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    technical_service_customer = fields.Boolean("Customer", default=False)
    request_id = fields.One2many('technical_service.request', 'customer_id', string="Request")