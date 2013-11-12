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

import webapp2
import David

from David.python_objects import objects
from David.db import entities
import jsonpickle


class MainHandler(webapp2.RequestHandler):
    def get(self):

        # creating course templates
        zumba = objects.CourseTemplate("Zumba", "Funny course")
        yoga = objects.CourseTemplate("Yoga", "Stupid course")

        # creating a gym
        peer = entities.Gym(name="peer", gym_network="peer", address="TLV", courses=[zumba, yoga])
        parent_key = peer.put()

        # creating real courses
        zumba_yaron = objects.Course("Zumba", "Funny course", 1400, 1, 20, "yaron", "katom", [])
        yoga_bar = objects.Course("Yoga", "Stupid course", 1700, 1, 20, "yaron", "katom", [])

        # creating daily schedule
        sunday = objects.DailySchedule(1, [zumba_yaron, yoga_bar])

        # craeting Month Schedule
        november = entities.MonthSchedule(parent=parent_key)
        november.year = 2013
        november.month = 11
        november.schedule_table = [sunday]
        november.put()


        # get from the db the all the month schedules of peer's gym
        schedules = entities.MonthSchedule(parent=entities.Gym.query(entities.Gym.name == "peer"))

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
