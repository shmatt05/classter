from db import entities
from python_objects.objects import *
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

    def add_user_to_gym(self, user_id, first_name, last_name, email, phone):
        user = User(user_id, first_name, last_name, email, phone)
        if not user_id in self.gym.users_table:
            self.gym.users_table[user_id] = user
            user_credential_entity = entities.UserCredentials(id=user_id, gym_network=self.gym_network,
                                                              gym_branch=self.gym_branch)
            user_credential_entity.set_key()
            user_credential_entity.put()
            self.gym.put()

    def add_user_to_course(self, course_id, user_id, year, month, day_in_month):
        month_sched = self.__get_month_schedule(month, year)
        course = self.get_course(course_id, year, month, day_in_month)
        code = course.try_register_user_to_course(user_id, year, month, day_in_month)
        month_sched.put()
        return code

    def delete_user_from_course(self, course_id, user_id, year, month, day_in_month):
        month_sched = self.__get_month_schedule(month, year)
        course =  self.get_course(course_id, year, month, day_in_month)
        if course.does_user_already_registered(user_id):
            course.remove_user_from_course(user_id)
            month_sched.put()

    def add_user_to_waiting_list_table(self, course_id, user_id, year, month, day_in_month):
        pass

    def delete_user_to_from_waiting_list_table(self, course_id, user_id, year, month, day_in_month):
        pass

    def delete_course_instance(self, class_key, year, month, day):
        month_sched = self.__get_month_schedule(month, year)
        daily_sched = month_sched.daily_schedule_table[str(day)]
        daily_sched.delete_course(class_key)
        month_sched.put()

    def delete_user_from_gym(self, user_id):
        if user_id in self.gym.users_table:
            del self.gym.users_table[user_id]
            self.gym.put()

    def edit_user(self, user_id, first_name, last_name, email, phone):
        user = User(user_id, first_name, last_name, email, phone)
        if user_id in self.gym.users_table:
              self.gym.users_table[user_id] = user
              self.gym.put()

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

    def create_gym(self,gym_network, gym_branch, address="", courses={}, instructors={}, studios=[], users_table={}):
        gym_entity = entities.Gym(name=gym_branch, gym_network=gym_network, address=address,
                                       courses=courses, instructors=instructors, studios=studios,
                                       users_table=users_table)
        gym_entity.set_key()
        gym_entity.put()
        return gym_entity

    def edit_course_time(self, course_id,year, month, day_in_month, start_hour, duration):
        # get the right month schedule
        month_schedule = self.__get_month_schedule(int(month), int(year))
        month_schedule_manager = MonthScheduleManager(month_schedule)
        #get the right daily schedule
        daily_schedule = month_schedule_manager.get_daily_schedule(day_in_month)
        #get the course from that daily schedule
        course = daily_schedule.get_course_by_id(course_id)
        if not course.hour == start_hour:
            course.hour = start_hour
            course.milli = course.to_mili(year, month, day_in_month)
        course.duration = duration
        #call the edit course function
        month_schedule.put()

    def edit_course_time_and_day(self, course_id, old_year, old_month, old_day, new_year, new_month, new_day,
                                 start_hour, duration):
        old_month_schedule = self.__get_month_schedule(int(old_month), int(old_year))
        new_month_schedule = old_month_schedule
        if old_month != new_month or old_year != new_year:
            new_month_schedule = self.__get_month_schedule(int(new_month), int(new_year))
        old_month_schedule_manager = MonthScheduleManager(old_month_schedule)
        new_month_schedule_manager = MonthScheduleManager(new_month_schedule)

        daily_schedule = old_month_schedule_manager.get_daily_schedule(old_day)
        course = daily_schedule.get_course_by_id(course_id)
        daily_schedule.delete_course(course_id)
        course.hour = start_hour
        course.milli = course.to_mili(new_year, new_month, new_day)
        course.duration = duration
        daily_schedule = new_month_schedule_manager.get_daily_schedule(new_day)
        daily_schedule.add_course(course)
        #get the course from that daily schedule
        old_month_schedule.put()
        if old_month_schedule != new_month_schedule:
            new_month_schedule.put()


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
                                year, month, day_in_week):
        # check and get the course template of that course
        gym_manager = GymManager(self.gym_network, self.gym_branch)
        course_template = gym_manager.does_course_template_exist(name)
        if course_template is None:
            raise Exception("No such Course Template")
        month_schedule = self.__get_month_schedule(int(month), int(year))
        if month_schedule is None:
            raise Exception("No Month Schedule!") #may be changed in the future
        new_course = Course(str(course_template.name), str(course_template.description), hour, duration, max_capacity,
                            instructor, studio, color, users_table, waiting_list_table,
                            registration_days_before, registration_start_time, str(uuid.uuid4()), None)
        month_schedule_manager = MonthScheduleManager(month_schedule)
        month_schedule_manager.add_course_to_month(new_course, day_in_week)
        #new_course.add_to_month_schedule(month_schedule, day)

    def create_course_instance(self, name, hour, duration, max_capacity, instructor, studio, color,
                                users_table, waiting_list_table, registration_days_before, registration_start_time,
                                year, month, day_in_month):
        gym_manager = GymManager(self.gym_network, self.gym_branch)
        course_template = gym_manager.does_course_template_exist(name)
        if course_template is None:
            raise Exception("No such Course Template")
        month_schedule = self.__get_month_schedule(int(month), int(year))
        if month_schedule is None:
            raise Exception("No Month Schedule!") #may be changed in the future
        new_course = Course(str(course_template.name), str(course_template.description), hour, duration, max_capacity,
                            instructor, studio, color, users_table, waiting_list_table,
                            registration_days_before, registration_start_time, str(uuid.uuid4()), None)
        month_schedule_manager = MonthScheduleManager(month_schedule)
        month_schedule_manager.add_course_instance(new_course, day_in_month)


    def edit_course(self,course_key, name, duration, max_capacity, instructor, studio,
                                 registration_days_before, registration_start_time,
                                year, month, day_in_month):
        month_schedule = self.__get_month_schedule(month, year)
        course = self.get_course(course_key,year,month,day_in_month)
        if not course in None:
            course.name = name
            course.duration = duration
            course.max_capacity = max_capacity
            course.instructor = instructor
            course.studio = studio
            course.registration_days_before = registration_days_before
            course.registration_start_time = registration_start_time
            month_schedule.put()

    """ for a given datetime object returns the daily schedule of all the days on the same week (sunday to saturday) """
    def get_weekly_daily_schedule_list_by_date(self, date_time):
        day_num = 7 if date_time.weekday() == 5 else (date_time.weekday()+2) % 7
        date_time = datetime.datetime(date_time.year, date_time.month, date_time.day)
        sunday = Time.get_sunday_of_week_containing_datetime(date_time, day_num)
        saturday = Time.get_saturday_of_week_containing_datetime(date_time, day_num)
        # TODO: export the methods out of DailyScheduleManager
        self.create_month_schedule(sunday.year,sunday.month)
        self.create_month_schedule(saturday.year, saturday.month)
        gym_manager = GymManager(self.gym_network,self.gym_branch)
        daily_sched_lst = gym_manager.get_daily_schedule_list(sunday, saturday)
        for daily_sched in daily_sched_lst:
            for course in daily_sched.courses_list:
                course.is_registration_open = course.is_registration_open_now(daily_sched.year,
                                                                          daily_sched.month, daily_sched.day_in_month)
        #return gym_manager.get_daily_schedule_list(sunday, saturday)
        return daily_sched_lst

    def get_registered_users_list_from_course(self, class_key, year, month, day_in_month):
        #month_schedule = self.__get_month_schedule(int(month), int(year))
        #month_schedule_manager = MonthScheduleManager(month_schedule)
        ##get the right daily schedule
        #daily_schedule = month_schedule_manager.get_daily_schedule(day_in_month)
        #course = daily_schedule.get_course_by_id(class_key)
        course = self.get_course(class_key, year, month, day_in_month)
        users_list = []
        if not course is None:
            for user_id in course.users_table.values():
                users_list.append(self.gym.users_table[user_id])
        return users_list

    def get_waiting_list_from_course(self, class_key, year, month, day_in_month):
        #month_schedule = self.__get_month_schedule(int(month), int(year))
        #month_schedule_manager = MonthScheduleManager(month_schedule)
        ##get the right daily schedule
        #daily_schedule = month_schedule_manager.get_daily_schedule(day_in_month)
        #course = daily_schedule.get_course_by_id(class_key)
        course = self.get_course(class_key, year, month, day_in_month)
        waiting_list = []
        for user_id in course.waiting_list_table.values():
            waiting_list.append(self.gym.users_table[user_id])
        return waiting_list

    """ returns the number of the day in range (1,7) by the given date """
    def get_day_by_date(self, year, month, day):
        temp_day = calendar.weekday(year, month, day)
        if temp_day == 5:
            return 7
        else:
            return (temp_day+2) % 7

    def get_users_of_gym(self):
        return self.gym.users_table

    def get_course(self, course_key, year, month, day_in_month):
        month_schedule = self.__get_month_schedule(int(month), int(year))
        month_schedule_manager = MonthScheduleManager(month_schedule)
        #get the right daily schedule
        daily_schedule = month_schedule_manager.get_daily_schedule(day_in_month)
        course = daily_schedule.get_course_by_id(course_key)
        return course

class AdminViewer:
    def __init__(self, gym_network, gym_branch):  # gym_key is <network>_<branch>
        self.gym_network = gym_network
        self.gym_branch = gym_branch

    def get_gym_info_for_popup(self):
        return GymManager(self.gym_network, self.gym_branch)



