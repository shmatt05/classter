from datetime import timedelta
from datetime import datetime
from google.appengine.api import mail
from admin_logic.admin_manager import AdminManager
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



class UserBusinessLogic:
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

    #def register_to_course(self):
    #    if self.user_entity is None:
    #        return NO_SUCH_USER
    #    if self.daily_schedule_entity is None:
    #        return NO_DAILY_SCHEDULE
    #    "find the correct course"
    #    for course in self.daily_schedule_entity.courses_list:
    #        if course.id == self.course_id:
    #            if not course.did_course_time_pass(self.year, self.month, self.day):
    #                if course.did_registration_start(self.year, self.month, self.day):
    #                    if not course.is_full():
    #                        if not course.does_user_already_registered(self.user_id):
    #                            course.add_user_to_course(self.user_entity)
    #                            self.month_schedule_entity.put()
    #                            return USER_REGISTRATION_SUCCEEDED
    #                        else:
    #                            return USER_ALREADY_REGISTERED
    #                    else:
    #                        return COURSE_IS_FULL
    #                else:
    #                    return REGISTRATION_DID_NOT_START
    #            else:
    #                return COURSE_TIME_PASSED
    #        else:
    #            continue
    #    return NO_SUCH_COURSE

    def register_to_course(self):
        if self.user_entity is None:
            return NO_SUCH_USER
        if self.daily_schedule_entity is None:
            return NO_DAILY_SCHEDULE
        "find the correct course"
        course = self.daily_schedule_entity.get_course_by_id(self.course_id)
        if not course is None:
            code = course.try_register_user_to_course(self.user_id, self.year, self.month, self.day)
            if code == objects.USER_REGISTRATION_SUCCEEDED:
                self.month_schedule_entity.put()

                date =  self.day +"/"+ self.month +"/"+ self.year
                #get user email

                user_email = get_user_mail_by_id(self.user_id)
                send_email(user_email, self.user_id, course.name, str(course.hour) ,str(date))
                print (user_email, self.user_id, course.name, str(course.hour) ,str(date))
            return code
        else:
            return NO_SUCH_COURSE

    def cancel_course_registration(self):
        if self.user_entity is None:
            return NO_SUCH_USER
        if self.daily_schedule_entity is None:
            return NO_DAILY_SCHEDULE
        "find the correct course"
        course = self.daily_schedule_entity.get_course_by_id(self.course_id)
        if not course is None:
             if course.does_user_already_registered(self.user_id):
                course.remove_user_from_course(self.user_id)
                self.month_schedule_entity.put()
                return USER_REMOVED_FROM_COURSE_SUCCEEDED
             else:
                return USER_IS_NOT_REGISTERED
        else:
            return NO_SUCH_COURSE

    #def cancel_course_registration(self):
    #    if self.user_entity is None:
    #        return NO_SUCH_USER
    #    if self.daily_schedule_entity is None:
    #        return NO_DAILY_SCHEDULE
    #    "find the correct course"
    #    for course in self.daily_schedule_entity.courses_list:
    #        if course.id == self.course_id:
    #             if course.does_user_already_registered(self.user_id):
    #                course.remove_user_from_course(self.user_entity)
    #                self.month_schedule_entity.put()
    #                return USER_REMOVED_FROM_COURSE_SUCCEEDED
    #             else:
    #                return USER_IS_NOT_REGISTERED
    #    return NO_SUCH_COURSE



    def add_to_waiting_list_table(self):
        pass

class UserView:
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

    def get_course_by_id(self):
        if self.user_entity is None:
            return NO_SUCH_USER
        if self.daily_schedule_entity is None:
            return NO_DAILY_SCHEDULE
        "find the correct course"
        for course in self.daily_schedule_entity.courses_list:
            if str(course.id) == str(self.course_id):
                return course
        return None

    def get_view_code(self, course):
        if course is None:
            return NO_SUCH_COURSE
        if not course.did_course_time_pass(self.year, self.month, self.day):
            if course.did_registration_start(self.year, self.month, self.day):
                if course.does_user_already_registered(self.user_id):
                    return USER_ALREADY_REGISTERED
                else:
                    if course.is_full():
                        return COURSE_IS_FULL
                    else:
                        return USER_IS_NOT_REGISTERED
            else:
                return REGISTRATION_DID_NOT_START
        else:
            return COURSE_TIME_PASSED

    def get_num_open_slots(self):
        course = self.get_course_by_id()
        if not course is None:
            return course.get_num_open_slots()
        else:
            return None

def get_daily_schedule_from_gym(gym_network, gym_branch, year, month, day):
    daily_schedule_manager = DailyScheduleManager(gym_network,gym_branch)
    return daily_schedule_manager.get_daily_schedule(year, month, day)


def get_month_schedule_from_gym(gym_network, name, year, month):
    return entities.MonthSchedule.get_month_schedule_entity(month, year, gym_network, name)

def send_email(email, user_id, course_name,course_hour, course_date):
    user_address = email

    if not mail.is_email_valid(user_address):
        pass
    else:
        #confirmation_url = createNewUserConfirmation(self.request)
        sender_address = "classter.app@gmail.com"
        subject = "Confirm your registration to course: " + course_name
        body = """This is a confirmation email for user ID: %s.
`You are now registered to %s at %s on %s.""" % (user_id, course_name, course_hour, course_date)
        mail.send_mail(sender_address, user_address, subject, body)


def get_user_mail_by_id(user_id):
    user_credentials_from_db = entities.UserCredentials.get_user_entity(user_id)
    gym_network = user_credentials_from_db.gym_network
    gym_branch = user_credentials_from_db.gym_branch
    admin_manager = AdminManager(gym_network, gym_branch)
    users_table = admin_manager.get_users_of_gym()
    curr_user = users_table[user_id]
    return curr_user.email



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