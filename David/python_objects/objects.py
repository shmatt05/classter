class CourseTemplate:
    def __init__(self, name, description):
        #assert isinstance(name, str)
        #assert isinstance(description, str)
        self.name = name
        self.description = description

class Course(CourseTemplate):
    def __init__(self, name, description, hour, duration, max_capacity, instructor, studio, users_list):
        super(Course, self).__init__(name, description)
        self.hour = hour
        self.duration = duration
        self.max_capacity = max_capacity
        self.instructor = instructor
        self.studio = studio
        self.users_list = users_list
    # TODO add functions: register_user, unregister_user, isBooked, add_to_waiting_list ...

class DailySchedule():
    def __init__(self, day, courses_list):
        self.day = day
        self.courses_list = courses_list
