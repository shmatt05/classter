from google.appengine.ext import ndb
from David.model import properties

class Gym(ndb.Model):
    name = ndb.StringProperty()
    gym_network = ndb.StringProperty()
    address = ndb.StringProperty()
    #courses = properties.CourseTemplateProperty(repeated=True) @deprecated
    courses = properties.OurJsonProperty()


# it's parent is Gym
class MonthSchedule(ndb.Model):
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    schedule_table = properties.OurJsonProperty()

