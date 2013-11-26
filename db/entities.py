from google.appengine.ext import ndb
from db import properties
from python_objects.objects import *

DEFAULT_NETWORK = "network"
DEFAULT_BRANCH = "branch"
DEFAULT_MONTH = "mm"
DEFAULT_YEAR = "yyyy"


class Gym(ndb.Model):
    """ represent Gym entity """
    name = ndb.StringProperty(required=True)
    gym_network = ndb.StringProperty(required=True)
    address = ndb.StringProperty()
    courses = properties.OurJsonProperty()     # {}
    instructors = properties.OurJsonProperty() # {}
    studios = properties.OurJsonProperty()     # []

    def set_key(self):
        self.key = Gym.__generate_key(self.gym_network, self.name)

    @classmethod
    def get_key(cls, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
        #return ndb.Key(Gym, gym_network +'_' +gym_branch)
        return cls.__generate_key(gym_network, gym_branch)

    @classmethod
    def __generate_key(cls, gym_network, gym_branch):
        return ndb.Key(Gym, gym_network + '_' + gym_branch)


class MonthSchedule(ndb.Model):
    """ Month Schedule Entity. It's parent key is Gym """
    year = ndb.IntegerProperty(required=True)
    month = ndb.IntegerProperty(required=True)
    schedule_table = properties.OurJsonProperty() #schedule_table = {day_one.day : day_one,  day_two.day : day_two }

    """ must set year and month prior calling the function! """
    def set_key(self, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
         self.key = MonthSchedule.__generate_key(self.month, self.year, gym_network, gym_branch)

    @classmethod
    def get_key(cls, month=DEFAULT_MONTH, year= DEFAULT_YEAR, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
        #return ndb.Key(Gym, gym_network +'_' + gym_branch, MonthSchedule, month + '-' + year)
        return cls.__generate_key(month, year, gym_network, gym_branch)

    @classmethod
    def __generate_key(cls, month=DEFAULT_MONTH, year= DEFAULT_YEAR, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
         return ndb.Key(Gym, gym_network +'_' + gym_branch, MonthSchedule, str(month) + '-' + str(year))


class Users(ndb.Model):
    """ Users Entity. It's parent key is Gym """
    users_table = properties.OurJsonProperty()

    def create_users_table(self, *users):
        users_table = {}
        for user in users:
            assert (type(user) == User)
            users_table[user.id] = user
        return users_table

    def set_key(self, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
        self.key = ndb.Key(Gym, gym_network + '_' + gym_branch, Users, "Users")

