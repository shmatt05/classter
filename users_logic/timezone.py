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



