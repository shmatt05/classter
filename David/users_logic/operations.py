from datetime import datetime
from datetime import timedelta
from David.users_logic.timezone import Time
from David.python_objects import objects
from David.db import entities
__author__ = 'rokli_000'

class DailyScheduleManager:

    def __init__(self, gym_network,gym_branch):
        self.gym_network = gym_network
        self.gym_branch = gym_branch

    """ get a list of DailySchedule from today up to num_days """
    def get_daily_schedule_list_from_today(self, num_days):
        time = Time('Israel') #from pytz.all_timezones
        return self.get_daily_schedule_list(time.now().date(), time.get_date_with_delta(num_days-1).date())

    """get a list of this week DailySchedule starting from today"""
    def get_week_daily_schedule_list(self):
        return self.get_daily_schedule_list_from_today(7)

    """ get a list of DailySchedule from start date up to end_date """
    def get_daily_schedule_list(self, start_date, end_date):
        result = []
        days = end_date.day - start_date.day
        year = start_date.year
        month = start_date.month
        schedule = entities.MonthSchedule.get_key(str(month), str(year), self.gym_network, self.gym_branch).get()
        for day in range(days+1):
            curr_date = start_date + timedelta(day)
            if curr_date.month == month:
                result.append(schedule.schedule_table[str(curr_date.day)])
            else:
                year = start_date.year
                month = start_date.month
                schedule = entities.MonthSchedule.get_key(str(month), str(year), self.gym_network, self.gym_branch).get()
                result.append(schedule.schedule_table[str(curr_date.day)])
        return result

    def add_user_to_course(self, username, year, month, day, start_hour, course_name):
            #get the course
            month_schedule = entities.MonthSchedule.get_key(month,year,self.gym_network, self.gym_branch).get()
            day_schedule = month_schedule.schedule_table[str(day)]
            courses = day_schedule.courses_list
            for course in courses:
                if course.name.lower() == course_name.lower() and course.hour == start_hour:
                    user = objects.User(username,0,None,username)
                    if len(course.users_list) <course.max_capacity:
                        course.users_list.append(user)
                    else:
                        course.waiting_list.append(user)
                    month_schedule.put()
                    break





print str(11)+ "-" + str(2013)
time = Time('Israel')
today = time.now()
for day in range(7):
    curr_date = today + timedelta(day)
    print curr_date
print timedelta(3)
print range(7)
 #from pytz.all_timezones
print time.now().day - time.get_date_with_delta(-7).day
print time.now()
print time.get_date_with_delta(20)
