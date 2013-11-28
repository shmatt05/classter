from google.appengine.ext import ndb
import sys
sys.path.insert(0, 'libs')
import jsonpickle

""" implements JsonProperty using jsonpickle """
class OurJsonProperty(ndb.JsonProperty):
     def __init__(self, **kwds):
         super(OurJsonProperty, self).__init__(**kwds)

     def _validate(self, value):
         assert isinstance(value, object)

     def _to_base_type(self, value):
         return jsonpickle.encode(value)

     def _from_base_type(self, value):
         return  jsonpickle.decode(value)