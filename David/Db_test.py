__author__ = 'duvid'

from google.appengine.ext import ndb


class Gym(ndb.Model):
    name = ndb.StringProperty()
    chain = ndb.StringProperty()
    address = ndb.StringProperty()
    courses = ndb.StructuredProperty(Course, repeated=True)
    # consider to change the implementation of courses from python class to something like:
    # https://developers.google.com/appengine/docs/python/ndb/subclassprop
    # or use JsonProperty


class Users(ndb.Model):
    users_table = ndb.JsonProperty()


class MonthSchedule(ndb.Model):
    year = ndb.IndexProperty()
    month = ndb.IndexProperty()
    schedule_table = ndb.JsonProperty()


class Course(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()


class GymCourse(Course):
    def __init__(self, name, description, hour, duration, max_capacity, instructor, studio):
        super(GymCourse, self).__init__(name, description)
        self.hour = hour
        self.duration = duration
        self.max_capacity = max_capacity
        self.instructor = instructor
        self.studio = studio

    # TODO add functions: register_user, unregister_user, isBooked, add_to_waiting_list ...


class User():
    def __init__(self, user_id, level, google_fb, name):
        self.user_id = user_id
        self.level = level
        self.google_fb = google_fb
        self.name = name

    # TODO: add user's history.




