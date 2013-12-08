from db import entities
from python_objects.objects import *
from users_logic.user_manager import DailyScheduleManager
import uuid
import datetime

__author__ = 'rokli_000'

import calendar


class AdminManager:
    def __init__(self, gym_network, gym_branch):  # gym_key is <network>_<branch>
        self.gym_network = gym_network
        self.gym_branch = gym_branch
        gym_entity = self.__get_gym()
        if gym_entity is None:
            gym_entity = self.create_gym(gym_network, gym_branch)
        self.gym = gym_entity

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
        new_template = CourseTemplate(name, description)
        new_template.add_to_gym(self.gym)

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
    # TODO: the method above is not updated, courses in Gym is a dictionary, and we should implement an object method
    # TODO: add delete_course_template method

    """ adds a new instructor object to the instructors list of the specified Gym entity
        the method does nothing in case the instructor already exists
    """
    def add_instructor(self, id_num, first_name, last_name):
        if self.gym is None:
            raise Exception("No such Gym!")
        new_instructor = Instructor(id_num, first_name, last_name)
        new_instructor.add_to_gym(self.gym)

    """ deletes an instructor from the instructors dictionary of the specified Gym entity """
    def delete_instructor(self, id_num):
        if self.gym is None:
            raise Exception("No such Gym!")
        instructor = self.gym.instructors[id_num]
        instructor.delete_from_gym(self.gym)

    """ adds a new studio object to the studios list of the specified Gym entity
        the method does nothing in case the studio already exists
    """
    def add_studio(self, name):
        if self.gym is None:
            raise Exception("No such Gym!")
        new_studio = Studio(name)
        new_studio.add_to_gym(self.gym)

    """ edits an existing studio object in the studios list of the specified Gym entity """
    def edit_studio(self, current_name, new_name):
        if self.gym is None:
            raise Exception("No such Gym!")
        for studio in self.gym.studios:
            if current_name.lower() == studio.name.lower():
                studio.edit_gym_studio(self.gym, new_name)
    # TODO: add delete_studio method

    def create_gym(self,gym_network, gym_branch, address="", courses={}, instructors={}, studios=[]):
        gym_entity = entities.Gym(name=gym_branch, gym_network=gym_network, address=address,
                                       courses=courses, instructors=instructors, studios=studios)
        gym_entity.set_key()
        gym_entity.put()
        return gym_entity


    """ creates a new MonthSchedule entity for the given month and year with the current gym as its parent
        doesn't change the DB if the MonthSchedule already exists
    """
    def create_month_schedule(self, year, month):
        days_in_month = calendar.monthrange(year, month)[1]
        schedule = self.__get_month_schedule(month, year)
        if schedule is None:
            schedule = entities.MonthSchedule(year=year, month=month, daily_schedule_table={})
            schedule.set_key(self.gym_network, self.gym_branch)
            for day_of_month in range(1, days_in_month+1):
                daily_schedule = DailySchedule(year, month, day_of_month,
                                                       self.get_day_by_date(year, month, day_of_month), [])
                schedule.daily_schedule_table[day_of_month] = daily_schedule
            schedule.put()

    """ creates a new course object and updates the day that matches the given day in each week of the current month
        day should be in range(1,7)
    """
    def create_course_for_month(self, name, hour, duration, max_capacity, instructor, studio, color,
                                users_table, waiting_list_table, registration_days_before, registration_start_time,
                                year, month, day):
        # check and get the course template of that course
        gym_manager = GymManager(self.gym_network, self.gym_branch)
        course_template = gym_manager.does_course_template_exist(name)
        if course_template is None:
            raise Exception("No such Course Template")
        month_schedule = self.__get_month_schedule(month, year)
        if month_schedule is None:
            raise Exception("No Month Schedule!") #may be changed in the future
        new_course = Course(str(course_template.name), str(course_template.description), hour, duration, max_capacity,
                            instructor, studio, color, users_table, waiting_list_table,
                            registration_days_before, registration_start_time, str(uuid.uuid4()), None)
        month_schedule_manager = MonthScheduleManager(month_schedule)
        month_schedule_manager.add_course_to_month(new_course, day)
        #new_course.add_to_month_schedule(month_schedule, day)

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

    """ for a given datetime object returns the daily schedule of all the days on the same week (sunday to saturday) """
    def get_weekly_daily_schedule_list_by_date(self, date_time):
        day_num = 7 if date_time.weekday() == 5 else (date_time.weekday()+2) % 7
        sunday = Time.get_sunday_of_week_containing_datetime(date_time, day_num)
        saturday = Time.get_saturday_of_week_containing_datetime(date_time, day_num)
        # TODO: export the methods out of DailyScheduleManager
        return DailyScheduleManager.get_daily_schedule_list(sunday, saturday)

    #def __get_sunday_of_week_containing_datetime(date_time, day_num):
    #    return date_time + datetime.timedelta(1 - day_num)
    #
    #def __get_saturday_of_week_containing_datetime(date_time, day_num):
    #    return date_time + datetime.timedelta(7 - day_num)

    """ returns the number of the day in range (1,7) by the given date """
    def get_day_by_date(self, year, month, day):
        temp_day = calendar.weekday(year, month, day)
        if temp_day == 5:
            return 7
        else:
            return (temp_day+2) % 7