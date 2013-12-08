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
from users_logic.user_manager import UserOperation
from admin_logic.admin_manager import AdminManager
# inject './lib' dir in the path so that we can simply do "import ndb" 
# or whatever there's in the app lib dir.
if 'lib' not in sys.path:
    sys.path[0:0] = ['lib']

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
    
# Map URLs to handlers
routes = [
    Route('/authenticated', handler='handlers.RootHandler'),
    Route('/profile', handler='handlers.ProfileHandler', name='profile'),
    Route('/logout', handler='handlers.AuthHandler:logout', name='logout'),
    Route('/auth/<provider>',handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
    Route('/auth/<provider>/callback',handler='handlers.AuthHandler:_auth_callback', name='auth_callback'),
    Route('/sign_up',handler='handlers.RootHandler2'),
    Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',handler='handlers.VerificationHandler', name='verification'),
    Route('/login', 'handlers.LoginHandler', name='login'),
    Route('/signup', 'handlers.SignupHandler'),
    Route('/forgot', 'handlers.ForgotPasswordHandler', name='forgot'),
    Route('/password', 'handlers.SetPasswordHandler'),
    Route('/', 'handlers.MainHandler'),
    Route('/user', 'handlers.UserHandler'),
    Route('/admin', 'handlers.AdminHandler'),
    Route('/craete_monthly_schedule', 'handlers.CreateMonthSched'),
    Route('/create_month_year', 'handlers.CreateMonthYear'),
    Route('/add_course', 'handlers.AddCourse'),
    Route('/create_course', 'handlers.CreateCourse'),
    Route('/register_to_class', 'handlers.RegisterToClass' ),
    Route('/initial','handlers.InitialHandler'),
    Route('/add_user', 'handlers.AddUser'),
    Route('/signupopup', 'handlers.SignUpPopUp'),
    Route('/changeweek', 'handlers.ChangeWeek')
]

app = WSGIApplication(routes, config=app_config, debug=True)

