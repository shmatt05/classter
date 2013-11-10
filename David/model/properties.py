from google.appengine.ext import ndb
from David.model.models import *
from David.python_objects.objects import *

class CourseTemplateProperty(ndb.StructuredProperty):
    def __init__(self, **kwds):
         super(CourseTemplateProperty, self).__init__(CourseTemplateModel, **kwds)

    def _validate(self, value):
        assert isinstance(value, CourseTemplate)

    def _to_base_type(self, value):
        return CourseTemplateModel(name = value.name, description = value.description)

    def _from_base_type(self, value):
        return CourseTemplate(value.name, value.description)