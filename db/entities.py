from google.appengine.ext import ndb
from google.appengine.ext.db import StringProperty
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
    courses = properties.OurJsonProperty(default={})
    instructors = properties.OurJsonProperty(default={})
    studios = properties.OurJsonProperty(default=[])
    users_table = properties.OurJsonProperty(default={})

    def set_key(self):
        self.key = Gym.__generate_key(self.gym_network, self.name)

    @classmethod
    def get_key(cls, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
        #return ndb.Key(Gym, gym_network +'_' +gym_branch)
        return cls.__generate_key(gym_network, gym_branch)

    @classmethod
    def __generate_key(cls, gym_network, gym_branch):
        return ndb.Key(Gym, gym_network + '_' + gym_branch)

    def __str__(self):
        return "name= " + self.name + ", network= " + self.gym_network + ", address= " + self.address + ", courses= " +\
               str(self.courses) + ", instructors= " + str(self.instructors) + ", studios= " + str(self.studios)


class MonthSchedule(ndb.Model):
    """ Month Schedule Entity. It's parent key is Gym """
    year = ndb.IntegerProperty(required=True)
    month = ndb.IntegerProperty(required=True)
    daily_schedule_table = properties.OurJsonProperty() #schedule_table = {day_one.day : day_one,  day_two.day : day_two }

    """ must set year and month prior calling the function! """
    def set_key(self, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
         self.key = MonthSchedule.__generate_key(self.month, self.year, gym_network, gym_branch)

    @classmethod
    def get_key(cls, month=DEFAULT_MONTH, year= DEFAULT_YEAR, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
        return cls.__generate_key(month, year, gym_network, gym_branch)

    @classmethod
    def __generate_key(cls, month=DEFAULT_MONTH, year= DEFAULT_YEAR, gym_network=DEFAULT_NETWORK, gym_branch=DEFAULT_BRANCH):
         return ndb.Key(Gym, gym_network +'_' + gym_branch, MonthSchedule, str(month) + '-' + str(year))


class UserCredentials(ndb.Model):
    id = ndb.StringProperty()
    gym_network = ndb.StringProperty()
    gym_branch = ndb.StringProperty()
    google_id = ndb.StringProperty()
    facebook_id = ndb.StringProperty()

    def set_key(self):
        self.key = UserCredentials.__generate_key(self.id)

    @classmethod
    def get_key(cls, id):
        return cls.__generate_key(id)

    @classmethod
    def __generate_key(cls, id):
        return ndb.Key(UserCredentials, id)

    def get_gym_entity(self):
        gym_entity = Gym.get_key(self.gym_network, self.gym_branch).get()
        if gym_entity is None:
            raise Exception("No such gym")
        else:
            return gym_entity


class GoogleCredentials(ndb.Model):
    google_id = ndb.StringProperty()
    user_id = ndb.StringProperty()

    def set_key(self):
        self.key = GoogleCredentials.__generate_key(self.google_id)

    @classmethod
    def get_key(cls, google_id):
        return cls.__generate_key(google_id)

    @classmethod
    def __generate_key(cls, google_id):
        return ndb.Key(GoogleCredentials, google_id)

    def get_user_gym_entity(self):
        self.get_user_entity().get_gym_entity()

    def get_user_entity(self):
        UserCredentials.get_key(self.user_id).get()


class FacebookCredentials(ndb.Model):
    facebook_id = ndb.StringProperty()
    user_id = ndb.StringProperty()

    def set_key(self):
        self.key = FacebookCredentials.__generate_key(self.facebook_id)

    @classmethod
    def get_key(cls, facebook_id):
        return cls.__generate_key(facebook_id)

    @classmethod
    def __generate_key(cls, facebook_id):
        return ndb.Key(FacebookCredentials, facebook_id)

    def get_user_gym_entity(self):
        self.get_user_entity().get_gym_entity()

    def get_user_entity(self):
        UserCredentials.get_key(self.user_id).get()