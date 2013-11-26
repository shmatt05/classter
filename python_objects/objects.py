from calendar import monthrange
from datetime import date


class CourseTemplate(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def add_to_gym(self, gym_entity):
        if self.name in gym_entity.courses.keys():
            return
        gym_entity.courses[self.name] = self
        gym_entity.put()

    def __str__(self):
        return self.name + "; " + self.description

    def __repr__(self):
        return self.__str__()


class Course(CourseTemplate):
    def __init__(self, name, description, hour, duration, max_capacity, instructor, studio, color, users_list, waiting_list):
        super(Course, self).__init__(name, description)
        self.hour = hour
        self.duration = duration
        self.max_capacity = max_capacity
        self.instructor = instructor
        self.studio = studio
        self.color = color
        self.users_list = users_list
        self.waiting_list = waiting_list
    # TODO add functions: register_user, unregister_user, isBooked, add_to_waiting_list ...

    """ day should be in range 1-7 """
    def add_to_month_schedule(self, month_schedule, day):
        year = month_schedule.year
        month = month_schedule.month
        days_in_month = monthrange(year, month)[1]
        for i in range(1, 8):
            if date(year, month, i).isoweekday() % 7 + 1 == int(day):
                day = i
                break
        #calculate all the matching days of the current month
        days_to_update = [x for x in range(day, days_in_month+1) if (x-day) % 7 == 0]
        for i in days_to_update:
            for course in month_schedule.schedule_table[str(i)].courses_list:
                if course.name.lower() == self.name.lower() and course.hour == self.hour:
                    return
            month_schedule.schedule_table[str(i)].courses_list.append(self)
        month_schedule.put()

    def __str__(self):
        return super(Course, self).__str__() + \
            ", " + str(self.hour) + ", " + self.studio + ", " + str(self.max_capacity)

    def __repr__(self):
        return self.__str__()


class DailySchedule(object):
    def __init__(self, year, month, day_in_month,day_in_week, courses_list):
        self.year = year
        self.month = month
        self.day_in_month = day_in_month
        self.day_in_week = day_in_week
        self.courses_list = courses_list


class User(object):
    def __init__(self, id, level, google_fb, name):
        self.id = id
        self.level = level
        self.google_fb = google_fb
        self.name = name

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
                break
        gym_entity.put()
