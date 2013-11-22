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
        self.gym = self.__get_gym()

    def __get_gym(self):
        return entities.Gym.get_key(self.gym_network, self.gym_branch).get()

    def get_courses_templates(self):
        return self.gym.courses

    def get_instructors(self):
        return self.gym.instructors

    def get_studios(self):
        return self.gym.studios

    def __get_month_schedule(self, month, year):
        return entities.MonthSchedule.get_key(str(month), str(year), self.gym_network, self.gym_branch).get()

    """ adds a new course_template object to the courses list of the specified Gym entity
        the method does nothing in case the course_template already exists
    """
    def add_course_template(self, name, description):
        if self.gym is None:
            raise Exception("No such Gym!")
        new_template = objects.CourseTemplate(self.gym, name, description)
        new_template.add_to_gym()

    """ adds a new instructor object to the instructors list of the specified Gym entity
        the method does nothing in case the instructor already exists
    """
    def add_instructor(self, id_num, first_name, last_name):
        if self.gym is None:
            raise Exception("No such Gym!")
        new_instructor = objects.Instructor(self.gym, first_name, last_name)
        new_instructor.add_to_gym()

    """ adds a new studio object to the studios list of the specified Gym entity
        the method does nothing in case the studio already exists
    """
    def add_studio(self, name):
        if self.gym is None:
            raise Exception("No such Gym!")
        new_studio = objects.Studio(self.gym, name)
        new_studio.add_to_gym()

    """ edits an existing course_template object in the courses list of the specified Gym entity """
    def edit_course_template(self, previous_name, new_name, new_description):
        if self.gym is None:
            raise Exception("No such Gym!")
        for template in self.gym.courses:
            if previous_name.lower() == template.name.lower():
                if template.name != new_name or template.description != new_description:
                    template.name = new_name
                    template.description = new_description
                    self.gym.put()

    """ creates a new MonthSchedule entity for the given month and year with the current gym as its parent
        doesn't change the DB if the MonthSchedule already exists
    """
    def create_month_schedule(self, year, month):
        days_in_month = calendar.monthrange(year, month)[1]
        schedule = self.__get_month_schedule(month, year)
        if schedule is None:
            schedule = entities.MonthSchedule(year=year, month=month, schedule_table={})
            schedule.set_key(self.gym_network, self.gym_branch)
            for day in range(1, days_in_month+1):
                new_day = objects.DailySchedule(year, month, day, self.get_day_by_date(year, month, day), [])
                schedule.schedule_table[day] = new_day
            schedule.put()

    """ creates a new course object and updates the day that matches the given day in each week of the current month
        day should be in range(1,7)
    """
    def create_course_for_month(self, name, description, hour, duration, max_capacity, instructor, studio, color,
                                users_list, waiting_list, year, month, day):
        new_course = objects.Course(self.gym, name, description, hour, duration, max_capacity, instructor, studio, color,
                                    users_list, waiting_list)
        days_in_month = calendar.monthrange(year, month)[1]
        #calculte all the matching days of the current month
        days_to_update = [x for x in range(day, days_in_month+1) if (x-day) % 7 == 0]
        schedule = self.__get_month_schedule(month, year)
        if schedule is None:
            raise Exception("No Month Schedule!") #may be changed in the future
        for i in days_to_update:
            for course in schedule.schedule_table[str(i)].courses_list:
                if course.name == name and course.hour == hour:
                    return
            schedule.schedule_table[str(i)].courses_list.append(new_course)
        schedule.put()

    def edit_course(self, old_name, new_name,  old_hour, new_hour, description, duration, max_capacity, instructor,
                    studio, color, users_list, waiting_list, year, month, day):
        month_schedule = self.__get_month_schedule(month, year)
        day_schedule = month_schedule.schedule_table[day].courses_list
        for course in day_schedule:
            if course.name.lower() == old_name.lower() and course.hour == old_hour:
                course.name = new_name
                course.description = description
                course.hour = new_hour
                course.duration = duration
                course.max_capacity = max_capacity
                course.instructor = instructor
                course.studio = studio
                course.color = color
                course.users_list = users_list
                course.waiting_list = waiting_list
                month_schedule.put()

    """ returns the number of the day in range (1,7) by the given date """
    def get_day_by_date(self, year, month, day):
        return (calendar.weekday(year, month, day)+2) % 7
