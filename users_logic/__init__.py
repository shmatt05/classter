from datetime import datetime
import jsonpickle

__author__ = 'rokli_000'

date = datetime.now()
json = jsonpickle.encode(date)
regular = jsonpickle.decode(json)

if type(regular) == type(date):
    print(regular.day)