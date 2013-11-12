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
from google.appengine.ext import ndb
import jsonpickle

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

        # uploadin gyms to DB
        goactive.put()
        peer.put()

        # creating real courses
        zumba_yaron = objects.Course("Zumba", "Funny course", 1400, 1, 20, "yaron","Katom", [],[])
        yoga_bar = objects.Course("Yoga", "Stupid course", 1700, 1, 20, "yaron", "blue",[], [])

        # creating schedule
        schedule_peer = entities.MonthSchedule()
        #schedule_peer.key = get_month_schedule_key("01-2013", "peer")
        schedule_peer.set_key("01-2013", "peer_peer")
        schedule_peer.month = 1
        schedule_peer.year = 2013
        first_day = objects.DailySchedule(1, [zumba_yaron, yoga_bar])
        second_day = objects.DailySchedule(2, [zumba_yaron, yoga_bar])
        schedule_peer.schedule_table = [first_day, second_day]

        schedule_sav = entities.MonthSchedule()
        schedule_sav.month = 7
        schedule_sav.year = 2011
        schedule_sav.set_key("01-2013", "Go Active_savyonim")

        schedule_sav.put()
        schedule_peer.put()


        #result = get_month_schedule_key("01-2013", "peer").get()
        #if type(result.schedule_table[0]) == objects.DailySchedule:
        #    self.response.write("I'm Daily Sche........!!" + "<br/>")
        #self.response.write(str(result.schedule_table[0].courses_list[0].name) + "<br/>")




app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
