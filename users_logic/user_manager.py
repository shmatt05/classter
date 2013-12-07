from datetime import timedelta
from datetime import datetime
from db import entities
from python_objects import objects
from users_logic.timezone import Time

__author__ = 'rokli_000'


class DailyScheduleManager:

    def __init__(self, gym_network,gym_branch):
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

    def get_daily_schedule(self, year, month , day):
        date_time = datetime(int(year), int(month), int(day))
        daily_schedule = self.get_daily_schedule_list(date_time,date_time)[0]
        if daily_schedule is None:
            raise Exception("No such daily schedule")
        else:
            return daily_schedule

    """ get a list of DailySchedule from today up to num_days """
    def get_daily_schedule_list_from_today(self, num_days):
        time = Time('Israel') #from pytz.all_timezones
        return self.get_daily_schedule_list(time.now(), time.get_date_with_delta(num_days-1))

    def get_from_last_week_to_next_week(self):
        time = Time('Israel')
        return self.get_daily_schedule_list(time.get_date_with_delta(-7), time.get_date_with_delta(14))

    """get a list of this week DailySchedule starting from today"""
    def get_week_daily_schedule_list(self):
        return self.get_daily_schedule_list_from_today(7)

    """ get a list of DailySchedule from start date up to end_date """
    def get_daily_schedule_list(self, start_datetime, end_datetime):
        result = []
        days = DailyScheduleManager.get_days_difference(start_datetime, end_datetime)
        year = start_datetime.year
        month = start_datetime.month
        schedule = entities.MonthSchedule.get_key(str(month), str(year), self.gym_network, self.gym_branch).get()
        for day in range(days+1):
            curr_date = start_datetime + timedelta(day)
            if curr_date.month == month:
                result.append(schedule.daily_schedule_table[str(curr_date.day)])
            else:
                year = curr_date.year
                month = curr_date.month
                schedule = entities.MonthSchedule.get_key(str(month), str(year), self.gym_network, self.gym_branch).get()
                result.append(schedule.daily_schedule_table[str(curr_date.day)])
        return result

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
        self.daily_schedule_entity = get_daily_schedule_from_gym(self.gym_entity.gym_network, self.gym_entity.name,
                                                                 year, month, day)

    def register_to_course(self):
        if self.user_entity is None:
            return NO_SUCH_USER
        if self.daily_schedule_entity is None:
            return NO_DAILY_SCHEDULE
        "find the correct course"
        for course in self.daily_schedule_entity.courses_list:
            if course.id == self.course_id:
                if course.check_registration_started():
                    if not course.is_full():
                        if not course.does_user_already_registered(self.user_id):
                            course.add_user_to_course(self.user_id);
                        else:
                            return USER_ALREADY_REGISTERED
                    else:
                        return COURSE_IS_FULL
                else:
                    return REGISTRARION_DID_NOT_START
            else:
                return NO_SUCH_COURSE




    def cancel_course_registration(self):
        pass


def get_daily_schedule_from_gym(gym_network, gym_branch, year, month, day):
    daily_schedule_manager = DailyScheduleManager(gym_network,gym_branch)
    return daily_schedule_manager.get_daily_schedule(year, month, day)

NO_SUCH_USER = 100
NO_DAILY_SCHEDULE = 200
USER_ALREADY_REGISTERED = 300
COURSE_IS_FULL = 400
REGISTRARION_DID_NOT_START = 500
NO_SUCH_COURSE = 600