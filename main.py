#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from datetime import date, datetime

import webapp2
import cgi
import jinja2
import os
from David.users_logic import operations

from David.python_objects import objects
from David.db import entities
from David.users_logic import operations
from David.admin_logic.operations import AdminManager
from google.appengine.ext import ndb
import jsonpickle
from David.users_logic.timezone import Time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GYM_NAME = "default_gym"
DEFAULT_MONTH_YEAR = "01-2001"

class MainHandler(webapp2.RequestHandler):
    def get(self):

        peer = entities.Gym(name="peer", gym_network="peer", address="TLV", courses={}, instructors ={}, studios=[])
        peer.set_key()
        peer.put()

        admin_manager = AdminManager("peer", "peer")

        admin_manager.add_course_template("Zumba", "stupid course")
        admin_manager.add_course_template("Yoga", "ugly course")

        peer_gym_before = entities.Gym.get_key("peer", "peer").get()
        course_templates = peer_gym_before.courses
        self.response.write(str(course_templates) + "<br/>")

        hour = datetime.now().hour

        admin_manager.create_course_for_month("ZumbaLatis", "Latis the Zumbot", hour, 120, 10,
                              "Moished", "Park","blue", [], [], 2014, 2, 3)


        #creating course templates
        #zumba = objects.CourseTemplate("Zumba", "Funny course")
        #yoga = objects.CourseTemplate("Yoga", "Stupid course")

        # creating gyms

        #goactive = entities.Gym(name = "savyonim",gym_network="Go Active")

        #goactive.set_key()

        # uploading gyms to DB
        #goactive.put()


        #
        #admin = AdminManager("peer", "peer")
        #admin.add_course_template("yoga", "Zubin Meta")
        #admin.create_month_schedule(2014, 2)
        ##admin.edit_course_template("yoga","yoga11","Kaki batachton!")
        #admin.create_course_for_month("ZumbaLatis", "Latis the Zumbot", hour, 120, 10,
        #                              "Moished", "Park","blue", [], [], 2014, 2, 3)
        #day_number = admin.get_day_by_date(2013, 11, 7)
        #
        ## add user to zumbalatis
        #daily_sched_man = operations.DailyScheduleManager("peer", "peer")
        #daily_sched_man.add_user_to_course("Roy Klinger", 2014, 2, 3, hour, "ZumbaLatis")
        #daily_sched_man.add_user_to_course("Moshico Movshi", 2014, 2, 3, hour, "ZumbaLatis")
        #
        #daily = entities.MonthSchedule.get_key(2, 2014, "peer", "peer").get().schedule_table[str(3)]
        #for course in daily.courses_list:
        #    if course.name == "ZumbaLatis":
        #        self.response.write("before deletion: <br/>")
        #        for user in course.users_list:
        #            self.response.write("his name is: " + user.name + "<br/>")
        #
        #daily_sched_man.delete_user_from_course("Moshico Movshi", 2014, 2, 3, hour, "ZumbaLatis")
        #
        #daily1 = entities.MonthSchedule.get_key(2, 2014, "peer", "peer").get().schedule_table[str(3)]
        #for course in daily1.courses_list:
        #    if course.name == "ZumbaLatis":
        #        self.response.write("after deletion: <br/>")
        #        for user in course.users_list:
        #            self.response.write("his name is: " + user.name + "<br/>")
        #
        #peer_gym_after = entities.Gym.get_key("peer", "peer").get()
        #course_templates = peer_gym_after.courses
        #schedule = entities.MonthSchedule.get_key(2, 2014, "peer", "peer").get()
        #self.response.write(str(course_templates) + "<br/>")
        #self.response.write(str(schedule.schedule_table.keys()) + "<br/>")
        #self.response.write(str(schedule.schedule_table['3'].courses_list) + "<br/>")
        #self.response.write(str(day_number) + "<br/>")
        #
        ## creating real courses
        #zumba_yaron = objects.Course("Zumba", "Funny course", 1400, 60, 20, "yaron","Katom", "#FF99FF", [],[])
        #yoga_bar = objects.Course("Yoga", "Stupid course", 1700, 90, 90, "yaron", "blue", "#3399FF",[], [])
        #
        #
        ## creating schedule
        #schedule_peer = entities.MonthSchedule()
        #schedule_peer.month = 11
        #schedule_peer.year = 2013
        #schedule_peer.set_key("peer", "peer")
        #first_day = objects.DailySchedule(2013, 11, 1, 3, [zumba_yaron, yoga_bar])
        #second_day = objects.DailySchedule(2013, 11, 2, 5, [zumba_yaron, yoga_bar])
        #schedule_peer.schedule_table = {int(first_day.day_in_month): first_day, int(second_day.day_in_month): second_day}
        #
        #schedule_sav = entities.MonthSchedule()
        #schedule_sav.month = 7
        #schedule_sav.year = 2011
        #schedule_sav.set_key("Go Active", "savyonim")
        #
        #schedule_sav.put()
        #schedule_peer.put()
        #
        ##create users
        #david = objects.User(12342156, 3, 144221, "david")
        #matan = objects.User(12323126, 2, 1321, "matan")
        #omri = objects.User(123756456, 1, 1321, "omri")
        #roy = objects.User(123432356, 4, 1321, "roy")
        #
        #users = entities.Users()
        #users.set_key("peer", "peer")
        #users.users_table = users.create_users_table(david, matan, omri, roy)
        #users.put()
        #
        #users_manager = operations.DailyScheduleManager("peer", "peer")
        #start_date = datetime(day=1, month=11, year=2013)
        #end_date = datetime(day=2, month=11, year=2013)
        #
        #result = entities.MonthSchedule.get_key("11","2013","peer","peer").get()
        #if type(result.schedule_table[str(first_day.day_in_month)]) == objects.DailySchedule:
        #    self.response.write("I'm Daily Sche........!!" + "<br/>")
        #self.response.write(str(result.schedule_table[str(first_day.day_in_month)].day_in_month) + "<br/>")
        #self.response.write(str(users_manager.get_daily_schedule_list(start_date, end_date)[0].courses_list[0].studio))

#input: str == year#month#day#course_name#hour#studio
#output: list of [year, month, day, course_name, hour, studio]

def parse_course(str):
    return  str.split('#')


class TestHandler(webapp2.RequestHandler):
    def get(self):
        users_manager = operations.DailyScheduleManager("peer", "peer")
        start_date = datetime(day=1, month=11, year=2013)
        end_date = datetime(day=2, month=11, year=2013)
        sched = users_manager.get_week_daily_schedule_list()
        #sched = users_manager.get_daily_schedule_list(start_date, end_date)

        template_values = {
            'days': sched
        }

        template = JINJA_ENVIRONMENT.get_template('Matan/grid.html')
        self.response.write(template.render(template_values))


class CreateMonthSched(webapp2.RequestHandler):
    def post(self):
        full_date = cgi.escape(self.request.get('month'))
        date_arr = full_date.split('-')
        year = date_arr[0]
        month = date_arr[1]
        #self.response.write(date_arr)
        admin_man = AdminManager("peer","peer")
        admin_man.create_month_schedule(int(year), int(month))

        template_values = {
            'year': year,
            'month': month,
            'courses': admin_man.get_courses_templates()
        }
        template = JINJA_ENVIRONMENT.get_template('Matan/create_monthly_schedule.html')
        self.response.write(template.render(template_values))


class CreateMonthYear(webapp2.RequestHandler):

    def get(self):
        template_values = {

        }
        template = JINJA_ENVIRONMENT.get_template('Matan/choose_month_year.html')
        self.response.write(template.render(template_values))


class AddCourse(webapp2.RequestHandler):

    def post(self):
        course_name = cgi.escape(self.request.get('course_name'))
        description = cgi.escape(self.request.get('description'))

        admin_man = AdminManager("peer", "peer")
        admin_man.add_course_template(course_name, description)

        template_values = {
            'year': self.request.get('year'),
            'month': self.request.get('month'),
            'courses': admin_man.get_courses_templates()
        }

        template = JINJA_ENVIRONMENT.get_template('Matan/create_monthly_schedule.html')
        self.response.write(template.render(template_values))


class CreateCourse(webapp2.RequestHandler):
    def post(self):
        year = cgi.escape(self.request.get('year'))
        month = cgi.escape(self.request.get('month'))
        day = cgi.escape(self.request.get('day'))
        class_name = cgi.escape(self.request.get('classes'))
        studio = cgi.escape(self.request.get('studio'))
        instructor = cgi.escape(self.request.get('instructor'))
        start_hour = cgi.escape(self.request.get('start_hour'))
        end_hour = cgi.escape(self.request.get('end_hour'))
        capacity = cgi.escape(self.request.get('capacity'))
        schedule_man = operations.DailyScheduleManager("peer", "peer")

        admin_man = AdminManager("peer", "peer")
        #admin_man.get_courses_templates()[]
        #admin_man.create_course_for_month(class_name, description, start_hour, end_hour-start_hour,capacity,instructor
        #    ,studio,"blue",[],[], year,month, day)

        today = date(int(year), int(month),1)
        in_a_week = date(int(year),int(month),7)
        daily_scheduale_list = schedule_man.get_daily_schedule_list(today, in_a_week)
        courses = self.get_courses_list_from_daily_schedual_list(daily_scheduale_list)
        self.response.write("year = "+year + " month= "+ month+ " class= " + str(class_name) + " studio= "+
                             studio + " instructor= " + instructor + " start= " + start_hour +
                                 " end= " + end_hour + " capacity= " + capacity +"courses list= " + str(courses))

    def get_courses_list_from_daily_schedual_list(self, daily_schedual_list):
        result = []
        for daily in daily_schedual_list:
            result.extend(daily.courses_list)
        return result


class RegisterToClass(webapp2.RequestHandler):

    def post(self):
        template_values = {

        }
        full_name=cgi.escape(self.request.get('firstname'))
        class_key=cgi.escape(self.request.get('classkey'))
        self.response.write(1000)



#todo consider make users a property in gym
#todo consider make each user an entity instead of users_table

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/test', TestHandler),
    ('/craete_monthly_schedule', CreateMonthSched),
    ('/create_month_year', CreateMonthYear),
    ('/add_course', AddCourse),
    ('/create_course', CreateCourse),
    ('/register_to_class', RegisterToClass )
], debug=True)


