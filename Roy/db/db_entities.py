from google.appengine.ext import ndb

class Gym(ndb.Model):
    name = ndb.StringProperty()
    gym_network = ndb.StringProperty()
    address = ndb.StringProperty()
    courses = ndb.JsonProperty() #the courses templates

    @classmethod
    def get_gym_query(cls, name):
        return cls.query(cls.name == name)

    @classmethod
    def get_gym_by_name(cls, name):
        gym_query = cls.get_gym_query(name)
        #if gym_query.count() == 1:
        return gym_query.fetch()[1]
        #elif gym_query.count() == 0:
        #    return None
        #else:
        #    return Exception



# their parent is Gym
class Users(ndb.Model):
    users_table = ndb.JsonProperty()


# their parent is Gym
class MonthSchedule(ndb.Model):
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    schedule_table = ndb.JsonProperty()



#peer_cinema = Gym(name="Peer Cinema", gym_network="Peer Cinema", address="TLV", courses={
#    "yoga":  "hey",
#    "spinning": "hello"
#    })
#
#peer_cinema.put()





