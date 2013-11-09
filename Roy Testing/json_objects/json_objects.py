class GymClassTemplate():
    def __init__(self, name, description):
        self.name = name
        self.description = description


class GymClass(GymClassTemplate):
    def __init__(self, name, description, hour, duration, max_capacity, instructor, studio):
        super(GymClass, self).__init__(name, description)
        self.hour = hour
        self.duration = duration
        self.max_capacity = max_capacity
        self.instructor = instructor
        self.studio = studio

        # TODO add functions: register_user, unregister_user, isBooked, add_to_waiting_list ...

class User():
    def __init__(self, user_id, level, google_fb, name):
        self.user_id = user_id
        self.level = level
        self.google_fb = google_fb
        self.name = name

        # TODO: add user's history.
