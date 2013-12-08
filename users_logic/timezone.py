__author__ = 'rokli_000'
import sys
sys.path.insert(0, 'libs')


from datetime import datetime
from datetime import timedelta
from pytz.gae import pytz


class Time():
    """
    tz should be one of pytz.all_timezones
    """
    def __init__(self, tz=None):
        if tz is None:
            self.tz_time = None
        else:
            self.tz_time = pytz.timezone(tz)

    def now(self):
        return datetime.now(self.tz_time)

    """ return the date of now + delta """
    def get_date_with_delta(self, delta):
        return datetime.now(self.tz_time) + timedelta(delta)

    def __add__(self, day):
        return self.get_date_with_delta(day)

    @classmethod
    def get_sunday_of_week_containing_datetime(cls, date_time, day_num):
        return date_time + datetime.timedelta(1 - day_num)

    @classmethod
    def get_saturday_of_week_containing_datetime(cls, date_time, day_num):
        return date_time + datetime.timedelta(7 - day_num)

    @classmethod
    def get_days_difference(cls, start_datetime, end_datetime):
        if start_datetime > end_datetime:
            raise Exception("start_date is bigger than end_date")
        time_delta = end_datetime - start_datetime
        return time_delta.days
