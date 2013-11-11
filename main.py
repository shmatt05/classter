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

        zumba = objects.CourseTemplate("Zumba", "Funny course")
        yoga = objects.CourseTemplate("Yoga", "Stupid course")
        peer = entities.Gym(name="peer", gym_network="peer", address="TLV", courses=[zumba, yoga])


        #to_json = jsonpickle.encode(zumba)
        #self.response.write(to_json +"<br/>")
        #
        #back_to_py = jsonpickle.decode(to_json)
        #if (type(back_to_py) == objects.CourseTemplate):
        #    self.response.write("WOOWOWO!!")
        peer.put()

        results = entities.Gym.query(entities.Gym.name == "peer").fetch()

        self.response.write(str(type(results[0])) + "<br/>")

        if type(results[0].courses[0]) == type(results[0].courses[1]):
            self.response.write("WWWWWOOOOOWWWW")

        self.response.write(str(type(results[0].courses[0].name)) + "<br/>")

        self.response.write(results[0].courses[1].name + "<br/>")


        #json_classes = {"Yoga":  "stupid class", "Zumba" : "crazy class" , "Pilates" : "lazy class"}
      #  yoga = python_objects.GymClassTemplate("Yoga", "stupid class")
      #  zumba = python_objects.GymClassTemplate("Zumba", "crazy class")
      #  pilates = python_objects.GymClassTemplate("Pilates", "lazy class")
      #  py_objects = [yoga, zumba, pilates]
      #  gym_from_py = gym_linker.GymClassesTemplate.from_python_obj(py_objects)
      #  peer_cinema = db_entities.Gym(name="Peer Cinema", gym_network="Peer Cinema", address="TLV", courses=gym_from_py.json_gym_classes_template)
      #  self.response.write(peer_cinema)
      #  peer_cinema.put()
      #  obj = db_entities.Gym.get_gym_by_name("Peer Cinema")
      #  self.response.write(obj)
      #  gym = gym_linker.GymClassesTemplate.from_db_json(obj.courses)
      ##  gym = gym_linker.GymLinker.from_db_json(json_classes)
      #  for i in gym.gym_classes_template_list:
      #          self.response.write("name= " + i.name + ", description= " + i.description + "<br/>")
        #for key, val in gym_from_py.json_gym_classes_template.items():
        #    self.response.write("key= "+ key + ", value= " + val + "<br/>")




app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
