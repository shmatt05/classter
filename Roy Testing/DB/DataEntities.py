import webapp2
from google.appengine.ext import ndb




class Gym(ndb.Model):
    name = ndb.StringProperty()

class GymBranch(Gym):
    address = ndb.StringProperty()


