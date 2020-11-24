# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import date_utils
import pytz, datetime

class technicalServiceHoursReportWizard(models.TransientModel):
    _name = 'technical_service.hours_worked.report.wizard'
    _description = "Wizard: quick calculation of hours worked in the week."

    employee_id = fields.Many2one('res.users', string="Technician", required=True)
    week_number = fields.Integer(required=True)

    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'employee_id': self.employee_id.id, 'week_number': self.week_number, 'name': self.employee_id.name
            },
        }

        # ref `module_name.report_id` as reference.
        return self.env.ref('technical_service.hours_worked_report').report_action(self, data=data)

class ReportTechnicalServiceHoursReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.technical_service.hours_worked_report_view'

    def _get_report_values(self, docids, data=None):
        sum_normal_hours, sum_hours_nigth, sum_sunday_hours = float(), float(), float()
        overtime_normal_hours, overtime_nigth, overtime_sunday = float(), float(), float()
        employee_id, week_number = data['form']['employee_id'], data['form']['week_number']
        requests = self.env['technical_service.request'].search([
            ('user_id.id', '=', employee_id),
            ('from_week_number', '>=', week_number),
            ('to_week_number', '<=', week_number)
        ])
        docs = list()
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for request in requests:
            # Convert Fields.Datetime to Datetime
            start_date, end_date = self.convert_to_datetime(request.start_date, request.end_date, local)
            # Get Worked Hours
            if (request.from_week_number == week_number) \
                    and (request.to_week_number == week_number):
                list_worked_hours = self.get_worked_hours(start_date, end_date)
            else:
                list_worked_hours = list()
            """
                        Hours worked Monday through Saturday from 7:00 a.m. at 8:00 p.m.
                                                    &
                        Hours worked Monday through Saturday from 8:00 p.m. to 7:00 a.m.
                                                    &
                                        Hours worked on Sunday
            """
            normal_hours, hours_nigth, sunday_hours = self.check_worked_hours(
                list_worked_hours,
                week_days=[0, 1, 2, 3, 4, 5],
                start_hour=7,
                end_hour=20
            )
            sum_normal_hours += normal_hours
            sum_hours_nigth += hours_nigth
            sum_sunday_hours += sunday_hours
            docs.append({
                'start_date': request.start_date,
                'end_date': request.end_date,
                'worked_hours': request.worked_hours,
                'normal_hours': normal_hours,
                'hours_nigth': hours_nigth,
                'sunday_hours': sunday_hours
            })
        if sum_normal_hours > 48: overtime_normal_hours = sum_normal_hours - 48
        if sum_hours_nigth > 48: overtime_nigth = sum_hours_nigth - 48
        if sum_sunday_hours > 48: overtime_sunday = sum_sunday_hours - 48
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'name': data['form']['name'],
            'week_number': week_number,
            'overtime_normal_hours': overtime_normal_hours or 0,
            'overtime_nigth': overtime_nigth or 0,
            'overtime_sunday': overtime_sunday or 0,
            'docs': docs,
        }

    def convert_to_datetime(self, from_date, to_date, local):
        start_date = datetime.datetime.strptime(
            fields.Datetime.to_string(from_date.astimezone(local)),
            '%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.strptime(
            fields.Datetime.to_string(to_date.astimezone(local)),
            '%Y-%m-%d %H:%M:%S')
        return start_date, end_date

    def get_worked_hours(self, start_date, end_date):
        """
                        The dictionary of hours worked is composed:
                days of the week as keys and a list of hours worked as values.
                        dict = {days of the week: [hours worked]}
        """
        count = 1
        list_hours = [start_date]
        if end_date:
            while True:
                temp_date = date_utils.start_of(start_date, "hour") + datetime.timedelta(hours=count)
                if temp_date < end_date:
                    list_hours.append(temp_date)
                    count += 1
                else: break
        list_hours.append(end_date)
        return list_hours

    def check_worked_hours(self, list_worked_hours, week_days, start_hour, end_hour):
        count_normal_hours = 0
        count_night_hours = 0
        count_sunday_hours = 0
        #         # Normal hours, Nigth Hours and Sunday
        #         # 7 AM <= x & x <= 8 PM include datetime current and next
        #         # 8 PM <= x & x <= 7 AM include datetime current and next
        for index, element in enumerate(list_worked_hours):
            if index == 0: continue
            old_datetime = list_worked_hours[index - 1]
            current_datetime = element
            from_hour = datetime.timedelta(hours=start_hour, minutes=0)
            to_hour = datetime.timedelta(hours=end_hour, minutes=0)
            if (old_datetime.weekday() in week_days) \
                    and (current_datetime.weekday() in week_days):
                if (from_hour <= datetime.timedelta(hours=old_datetime.hour, minutes=old_datetime.minute)) \
                        and (datetime.timedelta(hours=old_datetime.hour, minutes=old_datetime.minute) <= to_hour) \
                    and (from_hour <= datetime.timedelta(hours=current_datetime.hour, minutes=current_datetime.minute))\
                        and (datetime.timedelta(hours=current_datetime.hour, minutes=current_datetime.minute) <= to_hour):
                    delta = current_datetime - old_datetime
                    count_normal_hours += delta.total_seconds() / 3600
                else:
                    delta = current_datetime - old_datetime
                    count_night_hours += delta.total_seconds() / 3600

            else:
                delta = current_datetime - old_datetime
                count_sunday_hours += delta.total_seconds() / 3600
        return count_normal_hours, count_night_hours, count_sunday_hours