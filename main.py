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
import David

from David.python_objects import objects
from David.db import entities
from David.users_logic import operations
from google.appengine.ext import ndb
import jsonpickle
from David.users_logic.timezone import Time

DEFAULT_GYM_NAME = "default_gym"
DEFAULT_MONTH_YEAR = "01-2001"

class MainHandler(webapp2.RequestHandler):
    def get(self):

        #creating course templates
        zumba = objects.CourseTemplate("Zumba", "Funny course")
        yoga = objects.CourseTemplate("Yoga", "Stupid course")

        # creating gyms
        peer = entities.Gym(name="peer", gym_network="peer", address="TLV", courses=[zumba, yoga])
        goactive = entities.Gym(name = "savyonim",gym_network="Go Active")
        peer.set_key()
        goactive.set_key()

        # uploading gyms to DB
        goactive.put()
        peer.put()

        # creating real courses
        zumba_yaron = objects.Course("Zumba", "Funny course", 1400, 1, 20, "yaron","Katom", [],[])
        yoga_bar = objects.Course("Yoga", "Stupid course", 1700, 1, 20, "yaron", "blue",[], [])

        # creating schedule
        schedule_peer = entities.MonthSchedule()
        schedule_peer.month = 11
        schedule_peer.year = 2013
        schedule_peer.set_key("peer", "peer")
        first_day = objects.DailySchedule(1, [zumba_yaron, yoga_bar])
        second_day = objects.DailySchedule(2, [zumba_yaron, yoga_bar])
        schedule_peer.schedule_table = {int(first_day.day): first_day, int(second_day.day): second_day}

        schedule_sav = entities.MonthSchedule()
        schedule_sav.month = 7
        schedule_sav.year = 2011
        schedule_sav.set_key("Go Active", "savyonim")

        schedule_sav.put()
        schedule_peer.put()

        #create users
        david = objects.User(12342156, 3, 144221, "david")
        matan = objects.User(12323126, 2, 1321, "matan")
        omri = objects.User(123756456, 1, 1321, "omri")
        roy = objects.User(123432356, 4, 1321, "roy")

        users = entities.Users()
        users.set_key("peer", "peer")
        users.users_table = users.create_users_table(david,matan,omri,roy)
        users.put()

        users_manager = operations.DailyScheduleManager("peer", "peer")
        start_date = datetime(day=1, month=11, year = 2013)
        end_date = datetime(day=2, month=11, year = 2013)

        result = entities.MonthSchedule.get_key("11","2013","peer","peer").get()
        if type(result.schedule_table[str(first_day.day)]) == objects.DailySchedule:
            self.response.write("I'm Daily Sche........!!" + "<br/>")
        self.response.write(str(result.schedule_table[str(first_day.day)].day) + "<br/>")


        self.response.write(str(users_manager.get_daily_schedule_list(start_date, end_date)[0].courses_list[0].studio))



#todo consider make users a property in gym
#todo consider make each user an entity instead of users_table



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
