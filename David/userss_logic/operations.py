import pytz
from datetime import datetime
from datetime import timedelta
from David.userss_logic.timezone import Time

__author__ = 'rokli_000'

class DailyScheduleManager:

    def __init__(self, gym_key):
        self.gym_key = gym_key

    """ get a list of DailySchedule from today up to num_days """
    def get_daily_schedule_list_from_today(self, num_days):
        time = time = Time('Israel') #from pytz.all_timezones
        return self.get_daily_schedule_list(time.now().date(), time.get_date_with_delta(num_days-1).date())

    """get a list of this week DailySchedule starting from today"""
    def get_week_daily_schedule_list(self):
        return self.get_daily_schedule_list_from_today(7)

    """ get a list of DailySchedule from start date up to end_date """
    def get_daily_schedule_list(self, start_date, end_date):
        pass



time = time = Time('Israel') #from pytz.all_timezones
print time.now()
print time.get_date_with_delta(7)
