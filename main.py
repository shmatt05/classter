# -*- coding: utf-8 -*-
import sys
from secrets import SESSION_KEY

from webapp2 import WSGIApplication, Route
import handlers

from datetime import date, datetime, time
import cgi
import json
import sys

import webapp2
import jinja2


from users_logic.user_manager import DailyScheduleManager
from db import entities
from users_logic.user_manager import DailyScheduleManager
from users_logic.user_manager import UserBusinessLogic
from admin_logic.admin_manager import AdminManager
# inject './lib' dir in the path so that we can simply do "import ndb" 
# or whatever there's in the app lib dir.
import sys
sys.path.insert(0, 'libs')

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': [],
    'user_model': 'models.User',
  }
}


# ///////////////////////////////////////////////////////////

import os
from apiclient import discovery
from google.appengine.api import memcache
import webapp2
import jinja2
from oauth2client import appengine
import httplib2



#
#JINJA_ENVIRONMENT = jinja2.Environment(
#    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#    autoescape=True,
#    extensions=['jinja2.ext.autoescape'])
#
## CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
## application, including client_id and client_secret, which are found
## on the API Access tab on the Google APIs
## Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'python_objects/client_secrets.json')

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


#///////////////////////////////

# Map URLs to handlers
routes = [
    Route('/authenticated', handler='handlers.RootHandler'),
    Route('/profile', handler='handlers.ProfileHandler', name='profile'),
    Route('/logout', handler='handlers.AuthHandler:logout', name='logout'),
    Route('/auth/<provider>',handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
    Route('/auth/<provider>/callback',handler='handlers.AuthHandler:_auth_callback', name='auth_callback'),
    Route('/sign_up',handler='handlers.CheckIdHandler'),
    Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler='handlers.VerificationHandler', name='verification'),
    Route('/login', 'handlers.LoginHandler', name='login'),
    Route('/sign_up',handler='handlers.CheckIdHandler'),
    Route('/forgot', 'handlers.ForgotPasswordHandler', name='forgot'),
    Route('/password', 'handlers.SetPasswordHandler'),
    Route('/', 'handlers.MainHandler'),
    Route('/user', 'handlers.UserHandler'),
    Route('/admin', 'handlers.AdminHandler'),
    Route('/craete_monthly_schedule', 'handlers.CreateMonthSched'),
    Route('/create_month_year', 'handlers.CreateMonthYear'),
    Route('/add_course', 'handlers.AddCourse'),
    Route('/create_course', 'handlers.CreateCourse'),
    Route('/register_to_class', 'handlers.RegisterToClass'),
    Route('/new_initial','handlers.InitialHandler'),
    Route('/add_user', 'handlers.AddUser'),
    Route('/signupopup', 'handlers.SignUpPopUp'),
    Route('/changeweek', 'handlers.ChangeWeek'),
    Route('/newcoursepopup', 'handlers.NewCoursePopup'),
    Route('/id_page', 'handlers.IdPageHandler'),
    Route('/sign_in_successfully', 'handlers.SignInSuccessfullyHandler'),
    Route('/signup', 'handlers.SignupHandler'),
    Route('/add_class_to_schedule', 'handlers.AddClassToSched'),
    Route('/editcoursetime', 'handlers.EditCourseTime'),
    Route('/editcoursepopup','handlers.EditCoursePopup'),
    Route('/managecoursepopup','handlers.ManageCoursePopup'),

    Route('/remove_user_from_class', 'handlers.RemoveUserFromClass'),
    Route('/get_all_users', 'handlers.GetUsersList'),
    Route('/admin_register_to_course', 'handlers.AddUserToCourse'),
    Route('/admin_delete_from_course', 'handlers.RemoveUserFromCourse'),
    Route('/delete_course_instance', 'handlers.DeleteCourse'),
    Route('/edit_course_button_click', 'handlers.EditCourseButtonClick'),
    Route('/send_email', 'handlers.ConfirmUserRegistrationToClass'),
    Route('/user_auth', 'handlers.UserAuth'),

    Route('/add_instructor', 'handlers.AddInstructorToGym'),
    Route('/edit_instructor', 'handlers.EditInstructorToGym'),
    Route('/delete_instructor', 'handlers.DeleteInstructorToGym'),
    Route('/add_course_template', 'handlers.AddCourseTemplateToGym'),
    Route('/edit_course_template', 'handlers.EditCourseTemplateToGym'),
    Route('/delete_course_template', 'handlers.DeleteCourseTemplateToGym'),
    Route('/add_user_to_gym', 'handlers.AddUserToGym'),
    Route('/edit_user', 'handlers.EditUserToGym'),
    Route('/delete_user', 'handlers.DeleteUserToGym'),
    Route('/add_studio', 'handlers.AddStudioToGym'),
    Route('/edit_studio', 'handlers.EditStudioToGym'),
    Route('/delete_studio', 'handlers.DeleteStudioToGym'),
    Route('/create_event', 'handlers.CreateEventHandler'),
    Route(decorator.callback_path, decorator.callback_handler()),
]

app = WSGIApplication(routes, config=app_config, debug=True)

