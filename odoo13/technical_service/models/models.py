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
    hours_nigth = fields.Char('Hours at Nigth')

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
                # Convert Fields.Datetime to Datetime
                start_date, end_date = self.convert_to_datetime(record.start_date, record.end_date, local)
                # Get Worked Hours
                dict_worked_hours = self.get_worked_hours(start_date, end_date)


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
                # record.normal_hours = str(self.get_worked_hours(start_date, end_date)
                record.hours_nigth = self.get_worked_hours(start_date, end_date)
                record.normal_hours = self.check_normal_hours(dict_worked_hours)



                """
                    Hours worked Monday through Saturday from 8:00 p.m. to 7:00 a.m.
                """
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
        start_day = int(start_date.weekday())
        start_hour = int(start_date.hour)
        end_day = int(end_date.weekday())
        end_hour = int(end_date.hour)
        """
                                    The dictionary of hours worked is composed: 
                            days of the week as keys and a list of hours worked as values.                    
                                    dict = {days of the week: [hours worked]}
        """
        count = 1
        dict_hours = dict()
        for day in range(0, 7):
            list_hours = list()
            for hour in range(0, 24):
                temp_datetime = datetime.timedelta(days=day, hours=hour)
                if (temp_datetime >= datetime.timedelta(days=start_day, hours=start_hour)) \
                        and (temp_datetime < datetime.timedelta(days=end_day, hours=end_hour)):
                    list_hours.append(
                        date_utils.start_of(start_date, "hour") + datetime.timedelta(hours=count)
                    )
                    count += 1
            if day == start_day:
                list_hours.insert(0, start_date)
            if day == end_day:
                list_hours.append(end_date)
            if list_hours:
                dict_hours[day] = list_hours

        return dict_hours

    def convert_to_datetime(self, from_date, to_date, local):
        start_date = datetime.datetime.strptime(
            fields.Datetime.to_string(from_date.astimezone(local)),
            '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(
            fields.Datetime.to_string(to_date.astimezone(local)),
            '%Y-%m-%d %H:%M:%S')
        return start_date, end_date

    def check_normal_hours(self, dict_worked_hours):
        count = 0
        for day in dict_worked_hours.keys():
            for index, element in enumerate(dict_worked_hours[day]):
                if index == 0:
                    continue
                current_datetime = datetime.timedelta(
                    days=day,
                    hours=dict_worked_hours[day][index - 1].hour,
                    minutes=dict_worked_hours[day][index - 1].minute
                )
                next_datetime = datetime.timedelta(
                    days=day,
                    hours=element.hour,
                    minutes=element.minute
                )
                if (current_datetime >= datetime.timedelta(days=day, hours=7, minutes=0)) \
                        and (current_datetime <= datetime.timedelta(days=day, hours=20, minutes=0))\
                    and (next_datetime >= datetime.timedelta(days=day, hours=7, minutes=0))\
                        and (next_datetime <= datetime.timedelta(days=day, hours=20, minutes=0))\
                    and (day != 6):
                    delta = next_datetime - current_datetime
                    count += delta.total_seconds() / 3600

        return count