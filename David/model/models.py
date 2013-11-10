from google.appengine.ext import ndb

class CourseTemplateModel(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
