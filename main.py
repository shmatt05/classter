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

def gym_key(gym_name=DEFAULT_GYM_NAME):
    return ndb.Key(entities.Gym, gym_name)

def month_schedule_key(month_year=DEFAULT_MONTH_YEAR, gym_name = DEFAULT_GYM_NAME):
    return ndb.Key(entities.Gym, gym_name, entities.MonthSchedulel, month_year)



class MainHandler(webapp2.RequestHandler):
    def get(self):

        #creating course templates
        zumba = objects.CourseTemplate("Zumba", "Funny course")
        yoga = objects.CourseTemplate("Yoga", "Stupid course")

        # creating a gym)
        peer = entities.Gym(name="peer", gym_network="peer_another_one", address="TLV", courses=[zumba, yoga])
        peer.key = gym_key(peer.name)
        key = peer.put()
        if peer.key == key:
            self.response.write("WE ARE THE SAME!!!" +"<br/>")

        goactive = entities.Gym(gym_network="Go Active")
        goactive.key = gym_key("savyonim_goactive")

        goactive.put()

        schedule_peer = entities.MonthSchedule()#(parent=gym_key("peer"))
        schedule_peer.key = month_schedule_key("01-2013", "peer")

        #schedule_sav = entities.MonthSchedule(parent=gym_key("savyonim_goactive"))
        #schedule_sav.key = month_schedule_key("03_2013")



        schedule_peer.put()



        #schedule = entities.MonthSchedule(parent=gym_key("peer"))


        ## creating real courses
        #zumba_yaron = objects.Course("Zumba", "Funny course", 1400, 1, 20, "yaron", "katom", [])
        #yoga_bar = objects.Course("Yoga", "Stupid course", 1700, 1, 20, "yaron", "katom", [])
        #
        ## creating daily schedule
        #sunday = objects.DailySchedule(1, [zumba_yaron, yoga_bar])
        #
        ## craeting Month Schedule
        #november = entities.MonthSchedule(parent=parent_key)
        #november.year = 2013
        #november.month = 11
        #november.schedule_table = [sunday]
        #november.put()


        # get from the db the all the month schedules of peer's gym
        #schedules = entities.MonthSchedule(parent=entities.Gym.query(entities.Gym.name == "peer").fetch(1))

        #to_json = jsonpickle.encode(zumba)
        #self.response.write(to_json +"<br/>")
        #
        #back_to_py = jsonpickle.decode(to_json)
        #if (type(back_to_py) == objects.CourseTemplate):
        #    self.response.write("WOOWOWO!!")




        #results = entities.Gym.query(entities.Gym.name == "peer").fetch()
        #
        #self.response.write(str(type(results[0])) + "<br/>")
        #
        #if type(results[0].courses[0]) == type(results[0].courses[1]):
        #    self.response.write("WWWWWOOOOOWWWW")
        #
        #self.response.write(str(type(results[0].courses[0].name)) + "<br/>")
        #
        #self.response.write(results[0].courses[1].name + "<br/>")







app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
