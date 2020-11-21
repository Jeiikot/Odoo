# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.tools import date_utils
import pytz

import datetime


class technicalServiceStage(models.Model):
    """ Model for case stages. This models the main stages of a Technical Service Request management flow. """

    _name = 'technical_service.stage'
    _description = 'Technical Service Stage'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=20)
    done = fields.Boolean('Request Done')

class technicalServiceCategory(models.Model):
    _name = 'technical_service.category'
    _description = 'Technical Service Category'

    name = fields.Char('Name', required=True, translate=True)
    code = fields.Char('Code', required=True)


class technicalServiceRequest(models.Model):
    _name = 'technical_service.request'

    _description = 'Technical Service Request'

    @api.returns('self')
    def _default_stage(self):
        return self.env['technical_service.stage'].search([], limit=1)

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description')
    priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High')], string='Priority')
    worked_hours = fields.Float(string='Worked Hours',
        compute='_compute_worked_hours', store=True, readonly=True)

    normal_hours = fields.Char('Normal Hours')
    hours_nigth = fields.Float('Hours at Nigth')

    request_date = fields.Date('Request Date', tracking=True, default=fields.Date.context_today,
                               help="Date requested for the technical service to happen")
    schedule_date = fields.Datetime('Scheduled Date', required=True,
        help="Date the Technical Service team plans the service.  It should not differ much from the Request Date. ")
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    category_id = fields.Many2one('technical_service.category', string='Service Category', required=True)
    user_id = fields.Many2one('res.users', string='Technician', tracking=True, required=True)
    stage_id = fields.Many2one('technical_service.stage', string='Stage', ondelete='restrict',
                               tracking=True, default=_default_stage, copy=False)

    @api.onchange('schedule_date')
    def _onchange_start_date(self):
        # set auto-changing field
        self.start_date = self.schedule_date

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.end_date < record.start_date:
                raise exceptions.ValidationError(_("The start date must be less than the end date."))

    @api.constrains('stage_id', 'end_date')
    def _check_done(self):
        for record in self:
            if not record.end_date and record.stage_id.done == True:
                raise exceptions.ValidationError(_("The stage cannot be completed if there is no end date."))

    @api.depends('start_date', 'end_date')
    def _compute_worked_hours(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for record in self:
            if record.end_date and record.start_date:
                delta = record.end_date - record.start_date
                record.worked_hours = delta.total_seconds() / 3600.0

                start_date, end_date = self.convert_to_datetime(record.start_date, record.end_date, local)


                """
                    Hours worked Monday through Saturday from 7:00 a.m. at 8:00 p.m.
                """
                # if (start_date.hour >= 7.0 or end_date.hour < 20.0) and (start_date.weekday() != 6):
                #     if not start_date.hour >= 7.0:
                #         record.normal_hours = end_date.hour - 7
                #     if not end_date.hour < 20.0:
                #         record.normal_hours = 20 - start_date.hour
                #     if record.normal_hours < 0: record.normal_hours = 0
                # else:
                #     record.normal_hours = 0
                record.normal_hours = str(self.get_worked_hours(start_date, end_date))
                # record.normal_hours = str(date_utils.start_of(start_date, "hour") + datetime.timedelta(hours=5))

                # """
                #     Hours worked Monday through Saturday from 8:00 p.m. to 7:00 a.m.
                # """
                # if (start_date.hour >= 20.0 or end_date.hour < 7.0) and (start_date.weekday() != 6):
                #     if start_date.hour >= 20.0 and end_date < 7.0:
                #         record.hours_nigth = (23 - end_date.hour) - 20.0
                #     if (start_date.hour >= 0.0 and end_date.hour < 7.0) \
                #             or (start_date.hour > 20.0 and end_date.hour < 24.0):
                #         record.hours_nigth = end_date.hour - start_date.hour
                #     if record.hours_nigth < 0: record.hours_nigth = 0
                # else:
                #     record.hours_nigth = 0

            else:
                record.worked_hours = False


    def get_worked_hours(self, start_date, end_date):
        # start_day = int(start_date.weekday())
        # start_hour = int(start_date.hour)
        # end_day = int(end_date.weekday())
        # end_hour = int(end_date.hour)
        #
        # dict_hours = dict()
        # if start_day == end_day:
        #     dict_hours = {
        #         start_day: [hour for hour in range(start_hour, end_hour + 1)]
        #     }
        #     print(dict_hours)
        # else:
        #     for day in range(start_day, end_day + 1):
        #         if day == start_day:
        #             dict_hours[day] = [hour for hour in range(start_hour, 24)]
        #         if day == end_day:
        #             dict_hours[day] = [hour for hour in range(0, end_hour + 1)]
        #         if day != start_day and day != end_day:
        #             dict_hours[day] = [hour for hour in range(0, 24)]
        # return dict_hours
        count = 1
        list_hours = list()
        list_hours.append(start_date)
        while True:
            temp_hour = date_utils.start_of(start_date, "hour") + datetime.timedelta(hours=count)
            if temp_hour < end_date:
                list_hours.append(temp_hour)
            else:
                break
            count += 1
        list_hours.append(end_date)
        return list_hours

    def convert_to_datetime(self, from_date, to_date, local):
        start_date = datetime.datetime.strptime(
            fields.Datetime.to_string(from_date.astimezone(local)),
            '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(
            fields.Datetime.to_string(to_date.astimezone(local)),
            '%Y-%m-%d %H:%M:%S')
        return start_date, end_date