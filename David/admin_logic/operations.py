__author__ = 'rokli_000'

import calendar
from datetime import datetime
from David.db import entities
from David.python_objects import objects

class AdminManager:
    ' show in doc'
    def __init__(self, gym_network, gym_branch): #gym_key is <network>_<branch>
        self.gym_network = gym_network
        self.gym_branch = gym_branch

    """ adds a new course_template object to the courses list of the specified Gym entity
        the method does nothing in case the course_template already exists
    """
    def add_course_template(self, name, description):
        gym = entities.Gym.get_key(self.gym_network, self.gym_branch).get()
        for template in gym.courses:
            if name.lower() == template.name.lower():
                return
        new_template = objects.CourseTemplate(name, description)
        gym.courses.append(new_template)
        gym.put()

    def edit_course_template(self, previous_name, new_name, description):
        #check if exists
        #if previos_name == new_name then just update the description
        #check with the DB that description has been changed - if not, do nothing
        #in general, if the admin didn't changed anything the do nothing
        pass

    """ creates a new MonthSchedule entity for the given month and year with the current gym as its parent
        doesn't change the DB if the MonthSchedule already exists
    """
    def create_month_schedule(self, year, month):
        days_in_month = calendar.monthrange(year, month)[1]
        schedule = entities.MonthSchedule.get_key(str(month), str(year), self.gym_network, self.gym_branch).get()
        if schedule is None:
            schedule = entities.MonthSchedule(year=year, month=month, schedule_table={})
            schedule.set_key(self.gym_network, self.gym_branch)
            for day in range(1, days_in_month+1):
                new_day = objects.DailySchedule(day, [])
                schedule.schedule_table[day] = new_day
            schedule.put()

    """ creates a new course object and updates the day that matches the given day in each week of the current month
        day should be in range(1,7)
    """
    def create_course_for_month(self, name, description, hour, duration, max_capacity, instructor, studio, users_list,
                                waiting_list, day):
        new_course = objects.Course(name, description, hour, duration, max_capacity, instructor, studio, users_list,
                                    waiting_list)
        month = datetime.now().month
        year = datetime.now().year
        days_in_month = calendar.monthrange(year, month)[1]
        #calculte all the matching days of the current month
        days_to_update = [x for x in range(day, days_in_month+1) if (x-day) % 7 == 0]
        schedule = entities.MonthSchedule.get_key(str(month), str(year), self.gym_network, self.gym_branch).get()
        for i in days_to_update:
            schedule.schedule_table[i].courses_list.append(new_course)
        schedule.put()
