from google.appengine.api import mail
import os
from apiclient import discovery
from google.appengine.api import memcache
import webapp2
import jinja2
from oauth2client import appengine
import httplib2


__author__ = 'Omri'


class Email:
    def __init__(self):
        self.sender_address = "classter.app@gmail.com"


    def send_mail_gen(self, email, sender_address, subject, body, in_html):
        user_address = email

        if not mail.is_email_valid(user_address):
            pass
        else:
            mail.send_mail(sender_address, user_address, subject, body, html= in_html)


    def send_registration(self, email, user_id, course_name, course_hour, course_date):
        sender_address = "classter.app@gmail.com"
        subject = "Confirm your registration to course: " + course_name
        body = """This is a confirmation email for user ID: %s.
    `You are now registered to %s at %s on %s.""" % (user_id, course_name, course_hour, course_date)

        mail_html_body = """<!DOCTYPE html>
<html>
<head>
    <title>Confirm your registration to course: %s</title>
</head>
<body>
<h1>This is a confirmation email for user ID: %s.<h1>
</br>
<h3>You are now registered to %s at %s on %s.<h3>
<a href="http://www.pure.co.il/pure-gym.aspx"><img src="http://www.pure.co.il/images/opto-benyehuda.jpg"></a>
</body>
</html>""" % (course_name, user_id, course_name, course_hour, course_date)

        self.send_mail_gen(email, sender_address, subject, body, mail_html_body)

    def send_mail_to_group(self, email_arr, sender_address, subject, body):
        for i in range(len(email_arr)):
            user_address = email_arr[i]

            if not mail.is_email_valid(user_address):
                pass
            else:
                mail.send_mail(sender_address, user_address, subject, body)




class MyCalendar(webapp2.RequestHandler):


    JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        autoescape=True,
        extensions=['jinja2.ext.autoescape'])

    # CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
    # application, including client_id and client_secret, which are found
    # on the API Access tab on the Google APIs
    # Console <http://code.google.com/apis/console>
    CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '../../../Projects/google-workshop/python_objects/client_secrets.json')

    # Helpful message to display in the browser if the CLIENT_SECRETS file
    # is missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    <h1>Warning: Please configure OAuth 2.0</h1>
    <p>
    To make this sample run you will need to populate the client_secrets.json file
    found at:
    </p>
    <p>
    <code>%s</code>.
    </p>
    <p>with information found on the <a
    href="https://code.google.com/apis/console">APIs Console</a>.
    </p>
    """ % CLIENT_SECRETS

    http = httplib2.Http(memcache)
    service = discovery.build('calendar', 'v3', http=http)
    decorator = appengine.oauth2decorator_from_clientsecrets(
        CLIENT_SECRETS,
        scope=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.readonly',
        ],
        message=MISSING_CLIENT_SECRETS_MESSAGE)


    # The function that creates the event calendar object (dictionary)
    def get_calendar_event(self, title, location, year, month, day, start_hour, end_hour):
        event = {
            'summary': str(title),
            'location': str(location),
            'start': {
                'dateTime': "%s-%s-%sT%s:00" % (year, month, day, start_hour),
                'timeZone': 'Israel'
            },
            'end': {
                'dateTime': "%s-%s-%sT%s:00" % (year, month, day, end_hour),
                'timeZone': 'Israel'
            },
        }
        return event





    @decorator.oauth_required
    def update_calendar(self, gym_name , course_name, day, month, year, start_time, end_time ):
        event = self.get_calendar_event(course_name, gym_name, year, month, day, start_time, end_time)
        # Get the authorized Http object created by the decorator.
        http_page = self.decorator.http()
        # Call the service using the authorized Http object.
        response = self.service.events().insert(calendarId='primary', body=event).execute(http=http_page)
        if response['created'] is not None:
            #self.response.write("Created event successfully")
             self.redirect('/user')

