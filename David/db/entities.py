from google.appengine.ext import ndb
from David.model import properties

class Gym(ndb.Model):
    name = ndb.StringProperty()
    gym_network = ndb.StringProperty()
    address = ndb.StringProperty()
    courses = properties.CourseTemplateProperty(repeated=True)
