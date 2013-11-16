__author__ = 'rokli_000'

class AdminManager:
    ' show in doc'
    def __init__(self, gym_network, gym_branch): #gym_key is <network>_<branch>
        self.gym_network = gym_network
        self.gym_branch = gym_branch

    def add_course_template(self, name, description):
        #TODO implement

        #check if not already exists

        #update it by putting in the db the updated Gym entity

        pass

    def create_month_schedule(self, year, month):
        #TODO implement

        #check if not already exists

        #craete a new month_schedule for the month and year specified above for that specific gym

        #craete empty daily_schedules according to the number of days in that month

        #update the data base

        pass

    def create_course_for_month(self, name, description, hour, duration, max_capacity, instructor, studio, users_list, waiting_list, day):
        #TODO implement

        #create course object

        #get the right daily schedule

        #add the course created to the daily schedule courses_list

        #add the courese to the other daily_schedules of next week, 2 weeks from now and so on

        #updaete the data base by putting the month schedule containing the daily schedules above

        pass

