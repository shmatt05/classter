from calendar import monthrange
from datetime import date
from datetime import datetime, timedelta
import pytz
from db.entities import MonthSchedule, Gym
import uuid


import time
from users_logic.timezone import Time


class GymManager(object):
    def __init__(self, gym_network, gym_branch):
        self.gym_entity = Gym.get_gym_entity(gym_network, gym_branch)
        self.instructors_table = self.gym_entity.instructors
        self.courses_template_table = self.gym_entity.courses
        self.studios_list = self.gym_entity.studios

    def does_course_template_exist(self, course_name):
        course_templates_table = self.gym_entity.courses
        if course_templates_table is None:
            return None
        for item in course_templates_table.keys():
            if course_name.lower() == item.lower():
                return course_templates_table[item]

    """ get a list of DailySchedule from start date up to end_date """
    def get_daily_schedule_list(self, start_datetime, end_datetime):
        result = []
        days = Time.get_days_difference(start_datetime, end_datetime)
        year = start_datetime.year
        month = start_datetime.month
        schedule = MonthSchedule.get_month_schedule_entity(str(month), str(year),
                                                           self.gym_entity.gym_network, self.gym_entity.name)
        for day in range(days+1):
            curr_date = start_datetime + timedelta(day)
            if curr_date.month == month:
                result.append(schedule.daily_schedule_table[str(curr_date.day)])
            else:
                year = curr_date.year
                month = curr_date.month
                schedule = MonthSchedule.get_month_schedule_entity(str(month), str(year),
                                                                   self.gym_entity.gym_network, self.gym_entity.name)
                result.append(schedule.daily_schedule_table[str(curr_date.day)])
        return result

    """ get a list of DailySchedule from today up to num_days """
    def get_daily_schedule_list_from_today(self, num_days):
        time = Time('Israel')  # from pytz.all_timezones
        return self.get_daily_schedule_list(time.now(), time.get_date_with_delta(num_days-1))

    def get_from_last_week_to_next_week(self):
        time = Time('Israel')
        return self.get_daily_schedule_list(time.get_date_with_delta(-7), time.get_date_with_delta(14))

    """get a list of this week DailySchedule starting from today"""
    def get_week_daily_schedule_list(self):
        return self.get_daily_schedule_list_from_today(7)

    def get_daily_schedule(self, year, month, day):
        date_time = datetime(int(year), int(month), int(day))
        daily_schedule = self.get_daily_schedule_list(date_time, date_time)[0]
        if daily_schedule is None:
            raise Exception("No such daily schedule")
        else:
            return daily_schedule


class MonthScheduleManager(object):
    def __init__(self, month_schedule_entity):
        self.month_schedule = month_schedule_entity

    def add_course_to_month(self, course, day_in_week):
        year = self.month_schedule.year
        month = self.month_schedule.month
        days_in_month = get_num_of_days_in_month(year, month)
        for i in range(1, 8):
            if date(year, month, i).isoweekday() % 7 + 1 == int(day_in_week):
                day_in_week = i
                break
        #calculate all the matching days of the current month
        days_to_update = [x for x in range(day_in_week, days_in_month+1) if (x-day_in_week) % 7 == 0]
        for i in days_to_update:
            #for course in month_schedule.daily_schedule_table[str(i)].courses_list:
            #    if course.id == self.id:
            #        return
            new_course = Course(course.name, course.description, course.hour, course.duration, course.max_capacity,
                                course.instructor, course.studio, course.color, course.users_table,
                                course.waiting_list_table, course.registration_days_before,
                                course.registration_start_time, str(uuid.uuid4()), course.to_mili(year, month, i))
            #new_course.milli = new_course.to_mili(year, month, i, new_course)
            self.month_schedule.daily_schedule_table[str(i)].courses_list.append(new_course)
        self.month_schedule.put()

    def add_course_instance(self, course, day_in_month):
        year = self.month_schedule.year
        month = self.month_schedule.month
        new_course = Course(course.name, course.description, course.hour, course.duration, course.max_capacity,
                    course.instructor, course.studio, course.color, course.users_table,
                    course.waiting_list_table, course.registration_days_before,
                    course.registration_start_time, str(uuid.uuid4()), course.to_mili(year, month, day_in_month))
        self.month_schedule.daily_schedule_table[str(day_in_month)].courses_list.append(new_course)
        self.month_schedule.put()

    def get_daily_schedule(self, day_in_month):
        return self.month_schedule.daily_schedule_table[str(int(day_in_month))]

class CourseTemplate(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def add_to_gym(self, gym_entity):
        if self.name.lower() in [item.lower() for item in gym_entity.courses.keys()]:
            return
        gym_entity.courses[self.name] = self
        gym_entity.put()

    def __str__(self):
        return self.name + "; " + self.description

    def __repr__(self):
        return self.__str__()


class Course(CourseTemplate):
    def __init__(self, name, description, start_hour, duration, max_capacity, instructor, studio, color,
                 users_table, waiting_list_table, registration_days_before, registration_start_time, identifier,
                 start_milli, is_registration_open = False):
        super(Course, self).__init__(name, description)
        self.id = identifier
        self.hour = start_hour
        self.milli = start_milli
        self.duration = duration
        self.max_capacity = max_capacity
        self.instructor = instructor
        self.studio = studio
        self.color = color
        self.users_table = users_table
        self.waiting_list_table = waiting_list_table
        self.registration_days_before = registration_days_before
        self.registration_start_time = registration_start_time
        self.is_registration_open = is_registration_open
    # TODO add functions: unregister_user, isBooked, add_to_waiting_list ...

    """ day should be in range 1-7 """
    def add_to_month_schedule(self, month_schedule, day_in_week):
        year = month_schedule.year
        month = month_schedule.month
        days_in_month = monthrange(year, month)[1]
        for i in range(1, 8):
            if date(year, month, i).isoweekday() % 7 + 1 == int(day_in_week):
                day_in_week = i
                break
        #calculate all the matching days of the current month
        days_to_update = [x for x in range(day_in_week, days_in_month+1) if (x-day_in_week) % 7 == 0]
        for i in days_to_update:
            #for course in month_schedule.daily_schedule_table[str(i)].courses_list:
            #    if course.id == self.id:
            #        return
            new_course = Course(self.name, self.description, self.start_hour, self.duration, self.max_capacity,
                                self.instructor, self.studio, self.color, self.users_table, self.waiting_list_table,
                                self.registration_days_before, self.registration_start_time,
                                str(uuid.uuid4()), str(self.to_mili(year, month, i, self)))
            month_schedule.daily_schedule_table[str(i)].courses_list.append(new_course)
        month_schedule.put()

    def try_register_user_to_course(self, user_id, year, month, day):
        if not self.did_course_time_pass(year, month, day):
            if self.did_registration_start(year, month, day):
                if not self.is_full():
                    if not self.does_user_already_registered(user_id):
                        self.add_user_to_course(user_id)
                        return USER_REGISTRATION_SUCCEEDED
                    else:
                        return USER_ALREADY_REGISTERED
                else:
                    return COURSE_IS_FULL
            else:
                return REGISTRATION_DID_NOT_START
        else:
            return COURSE_TIME_PASSED

    def did_course_time_pass(self, year, month, day):
        now = Time('Israel').now()
        hour = self.__get_start_hour()
        minute = self.__get_start_minute()
        return now >= datetime(int(year), int(month), int(day), int(hour), int(minute),
                               0, 0, tzinfo=pytz.timezone("Israel"))

    def did_registration_start(self, year, month, day):
        if self.registration_days_before is None:
            return False
        course_date_time = datetime(int(year), int(month), int(day))
        registration_start_date_time = course_date_time - timedelta(int(self.registration_days_before))
        registration_start_date_time = datetime(registration_start_date_time.year, registration_start_date_time.month,
                                                registration_start_date_time.day, int(self.registration_start_time[:2]),
                                                int(self.registration_start_time[2:4]),0,0,pytz.timezone("Israel"))
        now = Time('Israel').now()
        return now >= registration_start_date_time

    def calculate_open_registration_date(self, year, month, day):
        if not self.did_registration_start(year, month, day):
            course_date_time = datetime(int(year), int(month), int(day))
            return course_date_time - timedelta(int(self.registration_days_before))

    def is_full(self):
        return len(self.users_table) >= int(self.max_capacity)

    def is_registration_open_now(self, year, month, day):
       try:
           return (not self.did_course_time_pass(year,month,day) and self.did_registration_start(year,month,day))
       except:
           return False

    def does_user_already_registered(self, user_id):
        if user_id in self.users_table:
            return True
        else:
            return False

    def add_user_to_course(self, user_id):
        self.users_table[user_id] = user_id

    def remove_user_from_course(self, user_id):
        del self.users_table[user_id]

    def get_num_open_slots(self):
        if self.is_full():
            return 0
        else:
            return int(self.max_capacity) - len(self.users_table)

    def __get_start_hour(self):
        return self.hour[:2]

    def __get_start_minute(self):
        return self.hour[2:4]

    def __str__(self):
        return super(Course, self).__str__() + \
            ", " + str(self.hour) + ", " + self.studio + ", " + str(self.max_capacity)

    def __repr__(self):
        return self.__str__()

    def to_mili(self, year, month, day_in_month):
        return long(time.mktime(datetime(int(year), int(month), int(day_in_month), int(self.__get_start_hour())-2,
                     int(self.__get_start_minute())).timetuple())*1000)


class DailySchedule(object):
    def __init__(self, year, month, day_in_month,day_in_week, courses_list):
        self.year = year
        self.month = month
        self.day_in_month = day_in_month
        self.day_in_week = day_in_week
        self.courses_list = courses_list

    def javascript_course_start_datetime(self, course):
        return time.mktime(datetime(int(self.year), int(self.month), int(self.day_in_month), int(course.hour[:2]),
                                    int(course.hour[2:4])).timetuple())*1000

    def get_course_by_id(self, course_id):
        for course in self.courses_list:
            if str(course.id) == course_id:
                return course
        return None

    def delete_course(self, course_id):
        self.courses_list = [course for course in self.courses_list if str(course.id) != str(course_id)]

    def add_course(self, course):
        self.courses_list.append(course)

class User(object):
    def __init__(self, id, first_name, last_name, email, phone):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        #self.histroy = history
        #self.level = level


        # TODO: add user's history.


class Instructor(object):
    def __init__(self, id_num, first_name, last_name):
        self.id_num = id_num
        self.first_name = first_name
        self.last_name = last_name

    def add_to_gym(self, gym_entity):
        if self.__is_instructor_in_gym(gym_entity):
            return
        else:
            # add instructor to the gym's instructors table
            gym_entity.instructors[self.id_num] = self
            gym_entity.put()

    def delete_from_gym(self, gym_entity):
        if not self.__is_instructor_in_gym(gym_entity):
            return # the instructor isn't in that gym so we can't delete it
        else:
            del gym_entity.instructors[self.id_num]
            gym_entity.put()

    """ check if instructor belong to the gym_entity and return true/false """
    def __is_instructor_in_gym(self, gym_entity):
        return self.id_num in gym_entity.instructors.keys()


class Studio(object):
    def __init__(self, name):
        self.name = name

    def add_to_gym(self, gym_entity):
        for studio in gym_entity.studios:
            if self.name.lower() == studio.name.lower():
                return
        gym_entity.studios.append(self)
        gym_entity.put()

    def edit_gym_studio(self, gym_entity, new_name):
        for studio in gym_entity.studios:
            if self.name.lower() == studio.name.lower():
                studio.name = new_name
                gym_entity.put()
                break

    def delete_from_gym(self, gym_entity):
        for studio in gym_entity.studios:
            if self.name.lower() == studio.name.lower():
                gym_entity.studios.remove(studio)
                gym_entity.put()
                break


def get_num_of_days_in_month(year, month):
    return monthrange(year, month)[1]


NO_SUCH_USER = 100
NO_DAILY_SCHEDULE = 200
USER_ALREADY_REGISTERED = 300
COURSE_IS_FULL = 400
REGISTRATION_DID_NOT_START = 500
NO_SUCH_COURSE = 600
COURSE_TIME_PASSED = 700
USER_REGISTRATION_SUCCEEDED = 800
USER_IS_NOT_REGISTERED = 900
USER_REMOVED_FROM_COURSE_SUCCEEDED = 1000