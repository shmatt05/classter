from google.appengine.ext import ndb
from David.db import properties
from David.python_objects import objects

DEFAULT_NETWORK = "network"
DEFAULT_BRANCH = "branch"
DEFAULT_MONTH = "mm"
DEFAULT_YEAR = "yyyy"

""" represent Gym entity """
class Gym(ndb.Model):
    name = ndb.StringProperty(required=True)
    gym_network = ndb.StringProperty(required=True)
    address = ndb.StringProperty()
    courses = properties.OurJsonProperty()

    def set_key(self):
        #self.key = ndb.Key(Gym, self.gym_network + '_' +self.name)
        self.key = Gym.__generate_key(self.gym_network, self.name)

    @classmethod
    def get_key(cls, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
        #return ndb.Key(Gym, gym_network +'_' +gym_branch)
        return cls.__generate_key(gym_network, gym_branch)

    @classmethod
    def __generate_key(cls, gym_network, gym_branch):
        return ndb.Key(Gym, gym_network +'_' +gym_branch)

""" Month Schedule Entity. It's parent key is Gym """
class MonthSchedule(ndb.Model):
    year = ndb.IntegerProperty(required=True)
    month = ndb.IntegerProperty(required=True)
    schedule_table = properties.OurJsonProperty() #schedule_table = {day_one.day : day_one,  day_two.day : day_two }

    """ must set year and month prior calling the functioin"""
    def set_key(self, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
         #self.key = ndb.Key(Gym, gym_network +'_' + gym_branch, MonthSchedule, str(self.month) + '-' + str(self.year))
          self.key = MonthSchedule.__generate_key(self.month, self.year, gym_network, gym_branch)

    @classmethod
    def get_key(cls, month=DEFAULT_MONTH, year= DEFAULT_YEAR, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
        #return ndb.Key(Gym, gym_network +'_' + gym_branch, MonthSchedule, month + '-' + year)
        return cls.__generate_key(month, year, gym_network, gym_branch)

    @classmethod
    def __generate_key(cls, month=DEFAULT_MONTH, year= DEFAULT_YEAR, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
         return ndb.Key(Gym, gym_network +'_' + gym_branch, MonthSchedule, str(month) + '-' + str(year))

""" Users Entity. It's parent key is Gym """
class Users(ndb.Model):
    users_table = properties.OurJsonProperty()

    def create_users_table(self, *users):
        users_table = {}
        for user in users:
            assert (type(user)==objects.User)
            users_table[user.id] = user
        return users_table

    def set_key(self, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
        self.key = ndb.Key(Gym, gym_network +'_' + gym_branch, Users, "Users")

