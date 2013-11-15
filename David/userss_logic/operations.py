import pytz
from datetime import datetime
from datetime import timedelta
from David.userss_logic.timezone import Time
from David.python_objects import objects
from David.db import entities
__author__ = 'rokli_000'

class DailyScheduleManager:

    def __init__(self, gym_key):
        self.gym_key = gym_key

    """ get a list of DailySchedule from today up to num_days """
    def get_daily_schedule_list_from_today(self, num_days):
        time = Time('Israel') #from pytz.all_timezones
        return self.get_daily_schedule_list(time.now().date(), time.get_date_with_delta(num_days-1).date())

    """get a list of this week DailySchedule starting from today"""
    def get_week_daily_schedule_list(self):
        return self.get_daily_schedule_list_from_today(7)

    """ get a list of DailySchedule from start date up to end_date """
    def get_daily_schedule_list(self, start_date, end_date):
        result = []
        days = end_date.day - start_date.day
        year = start_date.year
        month = start_date.month
        scheduale = entities.MonthSchedule.get_key(month +"-" +year, self.gym_key).get()
        for day in range(days):
            result.append(self, scheduale.schedule_table[day])


            start_date





print range(7)
time = Time('Israel') #from pytz.all_timezones
print time.now().day - time.get_date_with_delta(-7).day
print time.now()
print time.get_date_with_delta(20)
