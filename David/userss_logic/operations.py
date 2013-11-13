import pytz
from datetime import datetime
from datetime import timedelta
from David.userss_logic.timezone import Time

__author__ = 'rokli_000'

""" get a list of DailySchedule from today up to num_days """
def get_daily_schedule_list_from_today(num_days):
    time = Time('Israel') #from pytz.all_timezones
    print time.get_date_with_delta(19)
    return

"""get a list of this week DailySchedule starting from today"""
def get_week_daily_schedule_list():
    return get_daily_schedule_list(7)

""" get a list of DailySchedule from start date up to end_date """
def get_daily_schedule_list(start_date, end_date):
    pass



get_daily_schedule_list_from_today(7)