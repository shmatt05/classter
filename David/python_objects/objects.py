class CourseTemplate(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

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

    def __str__(self):
        return super(Course, self).__str__() + \
            ", " + str(self.hour) + ", " + self.studio + ", " + str(self.max_capacity)

    def __repr__(self):
        return self.__str__()

class DailySchedule(object):
    def __init__(self, day_in_month,day_in_week, courses_list):
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