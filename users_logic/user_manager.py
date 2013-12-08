from datetime import timedelta
from datetime import datetime
from db import entities
from python_objects import objects
from users_logic.timezone import Time

__author__ = 'rokli_000'


class DailyScheduleManager:

    def __init__(self, gym_network, gym_branch):
        self.gym_network = gym_network
        self.gym_branch = gym_branch
        gym_entity = entities.Gym.get_gym_entity(gym_network, gym_branch)
        if gym_entity is None:
            raise Exception("No such gym")
        self.gym = gym_entity

    """ returns the course corresponds to course_name and start_hour from courses_list"""
    @classmethod
    def get_specified_course(cls, course_name, start_hour, courses_list):
        for course in courses_list:
            if course.name.lower() == course_name.lower() and course.hour == start_hour:
                return course

    """ returns True if the user corresponds to username already subscribed to course """
    @classmethod
    def is_user_subscribed(cls, username, course):
        for user in course.users_list:
            if username == user.name:
                return True
        return False

    """ removes the user corresponds to username from the course's users_list """
    @classmethod
    def remove_user_from_class(cls, username, course):
        for user in course.users_list:
            if username == user.name:
                course.users_list.remove(user)

    def add_user_to_course(self, username, year, month, day, start_hour, course_name):
        #get the course
        print 'hello'
        month_schedule = entities.MonthSchedule.get_key(month, year, self.gym_network, self.gym_branch).get()
        day_schedule = month_schedule.daily_schedule_table[str(day)]
        courses = day_schedule.courses_list
        succeeded = 200
        for course in courses:
            if course.name.lower() == course_name.lower() and course.hour == start_hour:
                if DailyScheduleManager.is_user_subscribed(username, course):
                    return 300 #user already subscribed

                user = objects.User(username, 0, None, username)
                if len(course.users_list) < int(course.max_capacity):
                    course.users_list.append(user)
                    succeeded = 100
                else:
                    course.waiting_list.append(user)
                month_schedule.put()
                print 'succeeded = ' + str(succeeded) + ' length = ' + str(len(course.users_list)) + ' max = ' + str(course.max_capacity)
                return succeeded

    def delete_user_from_course(self, username, year, month, day, start_hour, course_name):
        month_schedule = entities.MonthSchedule.get_key(month, year, self.gym_network, self.gym_branch).get()
        day_schedule = month_schedule.daily_schedule_table[str(day)]
        courses = day_schedule.courses_list
        course = DailyScheduleManager.get_specified_course(course_name, start_hour, courses)
        if course is None:
            return
        DailyScheduleManager.remove_user_from_class(username, course)
        month_schedule.put()

    def add_user_to_course(self, user_id, course_id, year, month, day):
        #verify user in database

        #verify the user is allowed to take that course in that gym

        pass

    @classmethod
    def get_days_difference(cls, start_datetime, end_datetime):
        if start_datetime > end_datetime:
            raise Exception("start_date is bigger than end_date")
        time_delta = end_datetime - start_datetime
        return time_delta.days


class UserOperation:
    def __init__(self, user_id, course_id, year, month, day):
        self.user_id = user_id
        self.course_id = course_id
        self.year = year
        self.month = month
        self.day = day
        self.user_entity = entities.UserCredentials.get_user_entity(str(user_id))
        self.gym_entity = self.user_entity.get_gym_entity()# we get the gym from the user
        self.month_schedule_entity = get_month_schedule_from_gym(self.gym_entity.gym_network, self.gym_entity.name,
                                                                 year, month)
        self.daily_schedule_entity = self.month_schedule_entity.daily_schedule_table[str(day)]

    def register_to_course(self):
        if self.user_entity is None:
            return NO_SUCH_USER
        if self.daily_schedule_entity is None:
            return NO_DAILY_SCHEDULE
        "find the correct course"
        for course in self.daily_schedule_entity.courses_list:
            if course.id == self.course_id:
                if not course.did_course_time_pass(self.year, self.month, self.day):
                    if course.did_registration_start():
                        if not course.is_full():
                            if not course.does_user_already_registered(self.user_id):
                                course.add_user_to_course(self.user_entity)
                                self.month_schedule_entity.put()
                                return USER_REGISTRATION_SUCCEEDED
                            else:
                                return USER_ALREADY_REGISTERED
                        else:
                            return COURSE_IS_FULL
                    else:
                        return REGISTRATION_DID_NOT_START
                else:
                    return NO_SUCH_COURSE
            else:
                return COURSE_TIME_PASSED




    def cancel_course_registration(self):
        pass


def get_daily_schedule_from_gym(gym_network, gym_branch, year, month, day):
    daily_schedule_manager = DailyScheduleManager(gym_network,gym_branch)
    return daily_schedule_manager.get_daily_schedule(year, month, day)


def get_month_schedule_from_gym(gym_network, name, year, month):
    return entities.MonthSchedule.get_month_schedule_entity(month, year, gym_network, name)

NO_SUCH_USER = 100
NO_DAILY_SCHEDULE = 200
USER_ALREADY_REGISTERED = 300
COURSE_IS_FULL = 400
REGISTRATION_DID_NOT_START = 500
NO_SUCH_COURSE = 600
COURSE_TIME_PASSED = 700
USER_REGISTRATION_SUCCEEDED = 800