from google.appengine.ext import ndb
from David.db import properties

DEFAULT_GYM_KEY = "network_branch"
DEFAULT_MONTH_YEAR = "mm-yyyy"

""" represent Gym entity """
class Gym(ndb.Model):
    name = ndb.StringProperty(required=True)
    gym_network = ndb.StringProperty(required=True)
    address = ndb.StringProperty()
    courses = properties.OurJsonProperty()

    def set_key(self):
        self.key = ndb.Key(Gym, self.gym_network + '_' +self.name)

    @classmethod
    def get_key(cls,gym_network_and_name=DEFAULT_GYM_KEY):
        return ndb.Key(Gym, gym_network_and_name)


""" Month Schedule Entity. It's parent key is Gym """
class MonthSchedule(ndb.Model):
    year = ndb.IntegerProperty(required=True)
    month = ndb.IntegerProperty(required=True)
    schedule_table = properties.OurJsonProperty()

    def set_key(self, month_year=DEFAULT_MONTH_YEAR, gym_network_and_name=DEFAULT_GYM_KEY):
        self.key = ndb.Key(Gym, gym_network_and_name, MonthSchedule, month_year)

    @classmethod
    def get_key(cls, month_year=DEFAULT_MONTH_YEAR, gym_network_and_name=DEFAULT_GYM_KEY):
        return ndb.Key(Gym, gym_network_and_name, MonthSchedule, month_year)

""" Users Entity. It's parent key is Gym """
class Users(ndb.Model):
    users_table = properties.OurJsonProperty()

""" functions: """


#def get_gym_key(gym_name=DEFAULT_GYM_KEY):
#    return ndb.Key(Gym, gym_name)

#def get_month_schedule_key(month_year=DEFAULT_MONTH_YEAR, gym_name = DEFAULT_GYM_KEY):
#    return ndb.Key(Gym, gym_name, MonthSchedule, month_year)

