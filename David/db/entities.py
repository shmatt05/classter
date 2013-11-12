from google.appengine.ext import ndb
from David.db import properties

""" represent Gym entity """
class Gym(ndb.Model):
    name = ndb.StringProperty()
    gym_network = ndb.StringProperty()
    address = ndb.StringProperty()
    courses = properties.OurJsonProperty()

""" Month Schedule Entity. It's parent key is Gym """
class MonthSchedule(ndb.Model):
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    schedule_table = properties.OurJsonProperty()

""" Users Entity. It's parent key is Gym """
class Users(ndb.Model):
    users_table = properties.OurJsonProperty()

