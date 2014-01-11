# -*- coding: utf-8 -*-
import logging
import os
from tempfile import template
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
import secrets

import webapp2
from webapp2_extras import auth, sessions, jinja2
from jinja2.runtime import TemplateNotFound

from simpleauth import SimpleAuthHandler

from datetime import date, datetime, time, timedelta
import cgi
import json
import sys

import webapp2
from users_logic import user_manager

from users_logic.user_manager import DailyScheduleManager
from db import entities
from users_logic.user_manager import DailyScheduleManager
from users_logic.user_manager import UserBusinessLogic, UserView
from admin_logic.admin_manager import AdminManager, AdminViewer
from python_objects.objects import GymManager
import logging
import os
from tempfile import template
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
import secrets

import webapp2
from webapp2_extras import auth, sessions, jinja2
from jinja2.runtime import TemplateNotFound

from simpleauth import SimpleAuthHandler

from datetime import date, datetime, time, timedelta
import cgi
import json
import sys

import webapp2
from users_logic import user_manager

from users_logic.user_manager import DailyScheduleManager
from db import entities
from users_logic.user_manager import DailyScheduleManager
from users_logic.user_manager import UserBusinessLogic, UserView
from admin_logic.admin_manager import AdminManager, AdminViewer
from python_objects.objects import GymManager

import logging
import os
from tempfile import template
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
import secrets

import webapp2
from google.appengine.api import mail

import webapp2
from webapp2_extras import auth, sessions, jinja2
from jinja2.runtime import TemplateNotFound

from simpleauth import SimpleAuthHandler

from datetime import date, datetime, time
import cgi
import json
import sys

from users_logic.user_manager import DailyScheduleManager
from db import entities
from users_logic.user_manager import DailyScheduleManager
from admin_logic.admin_manager import AdminManager
from python_objects.objects import GymManager
from python_objects.user_notifications import MyCalendar
## check it ##
reload(sys)
sys.setdefaultencoding("utf-8")

########################



def user_required(handler):
    """
      Decorator that checks if there's a user associated with the current session.
      Will also fail if there's no session present.
    """

    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('login'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_login


class BaseRequestHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def jinja2(self):
        """Returns a Jinja2 renderer cached in the app registry"""
        return jinja2.get_jinja2(app=self.app)

    @webapp2.cached_property
    def session(self):
        """Returns a session using the default cookie key"""
        tmp_session = self.session_store.get_session()
        if tmp_session.get('curr_logged_in') == None:
            tmp_session['curr_logged_in'] = False
        if tmp_session.get('on_sign_up') == None:
            tmp_session['on_sign_up'] = False

        return tmp_session

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def current_user(self):
        """Returns currently logged in user"""
        user_dict = self.auth.get_user_by_session()
        return self.auth.store.user_model.get_by_id(user_dict['user_id'])

    @webapp2.cached_property
    def logged_in(self):
        """Returns true if a user is currently logged in, false otherwise"""
        #return self.auth.get_user_by_session() is not None
        #print(self.session.get('curr_user_id'))

        return self.session.get('curr_logged_in') == True

    def get_user_id(self):
        """Returns user ID"""
        return self.session.get('curr_user_id')

    def render(self, template_name, template_vars={}):
        # Preset values for the template
        values = {
            'url_for': self.uri_for,
            'logged_in': self.logged_in,
            'flashes': self.session.get_flashes(),
            'session': self.session
        }

        # Add manually supplied template values
        values.update(template_vars)

        # read the template or 404.html
        try:
            self.response.write(self.jinja2.render_template(template_name, **values))
        except TemplateNotFound:
            self.abort(404)

    def head(self, *args):
        """Head is used by Twitter. If not there the tweet button shows 0"""
        pass


    #############################################################

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.

        The list of attributes to store in the session is specified in
          config['webapp2_extras.auth']['user_attributes'].
        :returns
          A dictionary with most user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.

        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
          The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """
        return self.auth.store.user_model


    def display_message(self, message):
        """Utility function to display a template with a simple message."""
        params = {
            'message': message
        }
        self.render('message.html', params)

class UserAuth(BaseRequestHandler):
    def get(self):
        self.render('google_facebook_login.html')

class RootHandler(BaseRequestHandler):
    def get(self):
        """Handles default langing page"""
        self.render('home.html')


class ProfileHandler(BaseRequestHandler):
    def get(self):
        """Handles GET /profile"""
        on_sign_up = self.session.get('on_sign_up')
        #sing up
        if on_sign_up == True:
            if not user_has_session(self):
                error_message(self, 'We couldn\'t sign you up. Please try again.')

            if self.logged_in:
                sign_up_success(self)
            else:
                self.redirect('/')
        #sign in
        else:
            check_sign_in(self)


class AuthHandler(BaseRequestHandler, SimpleAuthHandler):
    """Authentication handler for OAuth 2.0, 1.0(a) and OpenID."""

    # Enable optional OAuth 2.0 CSRF guard
    OAUTH2_CSRF_STATE = True

    USER_ATTRS = {
        'facebook': {
            'id': lambda id: ('avatar_url',
                              'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
            'name': 'name',
            'link': 'link'
        },
        'google': {
            'picture': 'avatar_url',
            'name': 'name',
            'profile': 'link'
        },
        'windows_live': {
            'avatar_url': 'avatar_url',
            'name': 'name',
            'link': 'link'
        },
        'twitter': {
            'profile_image_url': 'avatar_url',
            'screen_name': 'name',
            'link': 'link'
        },
        'linkedin': {
            'picture-url': 'avatar_url',
            'first-name': 'name',
            'public-profile-url': 'link'
        },
        'linkedin2': {
            'picture-url': 'avatar_url',
            'first-name': 'name',
            'public-profile-url': 'link'
        },
        'foursquare': {
            'photo': lambda photo: ('avatar_url', photo.get('prefix') + '100x100' + photo.get('suffix')),
            'firstName': 'firstName',
            'lastName': 'lastName',
            'contact': lambda contact: ('email', contact.get('email')),
            'id': lambda id: ('link', 'http://foursquare.com/user/{0}'.format(id))
        },
        'openid': {
            'id': lambda id: ('avatar_url', '/img/missing-avatar.png'),
            'nickname': 'name',
            'email': 'link'
        }

    }

    def _on_signin(self, data, auth_info, provider):
        """Callback whenever a new or existing user is logging in.
         data is a user info dictionary.
         auth_info contains access token or oauth 0 and secret.
        """
        #valid_id(self)


        on_sign_up = self.session.get('on_sign_up')

        if on_sign_up == True:
            if not user_has_session(self):
                error_message(self, 'We couldn\'t sign you up. Please try again.')

        #signed_in = self.session.get('curr_logged_in')
        #if not signed_in:


        auth_id = '%s:%s' % (provider, data['id'])
        logging.info('Looking for a user with id %s', auth_id)
        self.session['connection'] = provider
        self.session['fb_g_o'] = data['id']
        self.session['user_email'] = data['email']
        ############################################################

        user = self.auth.store.user_model.get_by_auth_id(auth_id)
        _attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])

        if user:
            logging.info('Found existing user to log in')
            # Existing users might've changed their profile data so we update our
            # local model anyway. This might result in quite inefficient usage
            # of the Datastore, but we do this anyway for demo purposes.
            #
            # In a real app you could compare _attrs with user's properties fetched
            # from the datastore and update local user in case something's changed.
            user.populate(**_attrs)
            user.put()
            self.auth.set_session(
                self.auth.store.user_to_dict(user))

        else:
            # check whether there's a user currently logged in
            # then, create a new user if nobody's signed in,
            # otherwise add this auth_id to currently logged in user.

            if self.logged_in:
                logging.info('Updating currently logged in user')

                u = self.current_user
                u.populate(**_attrs)
                # The following will also do u.put(). Though, in a real app
                # you might want to check the result, which is
                # (boolean, info) tuple where boolean == True indicates success
                # See webapp2_extras.appengine.auth.models.User for details.
                u.add_auth_id(auth_id)

            else:
                logging.info('Creating a brand new user')
                ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
                if ok:
                    self.auth.set_session(self.auth.store.user_to_dict(user))

        # Remember auth data during redirect, just for this demo. You wouldn't
        # normally do this.
        self.session.add_flash(data, 'data - from _on_signin(...)')
        self.session.add_flash(auth_info, 'auth_info - from _on_signin(...)')

        if on_sign_up:
            sign_up_success(self)
        else:
            check_sign_in(self)
            # Go to the profile page
            #self.redirect('/profile')

    def logout(self):
        my_logout(self)

        self.auth.unset_session()

        self.redirect('/user')

    def handle_exception(self, exception, debug):
        logging.error(exception)
        self.render('error.html', {'exception': exception})

    def _callback_uri_for(self, provider):
        return self.uri_for('auth_callback', provider=provider, _full=True)

    def _get_consumer_info_for(self, provider):
        """Returns a tuple (key, secret) for auth init requests."""
        return secrets.AUTH_CONFIG[provider]

    def _to_user_model_attrs(self, data, attrs_map):
        """Get the needed information from the provider dataset."""
        user_attrs = {}
        for k, v in attrs_map.iteritems():
            attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
            user_attrs.setdefault(*attr)

        return user_attrs


class CheckIdHandler(BaseRequestHandler):
    def post(self):

        id = self.request.get('id')

        if not valid_id(id) or self.already_signup(id):
            error_message(self, 'We couldn\'t sign you up. Please try again.')
        else:
            self.session['on_sign_up'] = True
            self.session['curr_user_id'] = id
            self.render('sign_up.html')

            #def get(self):
            #    id = self.session.get('curr_user_id')
            #    if id is None:
            #        self.display_message('The ID: %s is not valid' % id)
            #        return
            #
            #    self.render('sign_up.html')

    def already_signup(self, user_id):
        user_from_db = entities.UserCredentials.get_user_entity(user_id)
        if (
                    user_from_db.google_id is not None or user_from_db.facebook_id is not None or user_from_db.self_registration_id is not None):
            return True
        else:
            return False


class IdPageHandler(BaseRequestHandler):
    def get(self):
        """Handles default langing page"""
        self.render('id_page.html')


class SignInSuccessfullyHandler(BaseRequestHandler):
    def get(self):
        """Handles default langing page"""
        #template_values = {
        #        'session': {
        #            'name': course.name,
        #            'studio': course.studio,
        #            'class_key': course.id,
        #            'color': course.color,
        #            'free_slots': course.get_num_open_slots(),
        #            'start_time': course.hour[:2] + ":" + course.hour[2:],
        #            'end_time': get_end_time(long(course.milli), course.duration)
        #        }
        self.render('sign_in_successfully.html')

        ##########################


class LoginHandler(BaseRequestHandler):
    def get(self):
        self._serve_page()

    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        email = self.request.get('email')
        #on_sign_up = self.session.get('on_sign_up')
        ##sing up
        #if on_sign_up == True:
        #    id = self.session.get('curr_user_id')
        #    if id is None:
        #        self.display_message('The ID: %s is not valid' % id)
        #        return

        try:
            u = self.auth.get_user_by_password(username, password, remember=True,
                                               save_session=True)

            self.session['connection'] = 'self'
            self.session['fb_g_o'] = username
            self.session['user_email'] = email
            check_sign_in(self)
            #self.redirect(self.uri_for('profile'))
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Login failed for user %s because of %s', username, type(e))
            self._serve_page(True)

    def _serve_page(self, failed=False):
        username = self.request.get('username')
        params = {
            'username': username,
            'failed': failed
        }
        self.render('login.html', params)


class VerificationHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        if not user_has_session(self):
            error_message(self, 'We couldn\'t sign you up. Please try again.')

        user = None
        user_id = kwargs['user_id']
        signup_token = kwargs['signup_token']
        verification_type = kwargs['type']
        #email = kwargs['email']

        # it should be something more concise like
        # self.auth.get_user_by_token(user_id, signup_token)
        # unfortunately the auth interface does not (yet) allow to manipulate
        # signup tokens concisely
        user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token, 'signup')

        if not user:
            logging.info('Could not find any user with id "%s" signup token "%s"',
                         user_id, signup_token)
            self.abort(404)

        # store user data in the session
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

        if verification_type == 'v':
            # remove signup token, we don't want users to come back with an old link
            self.user_model.delete_signup_token(user.get_id(), signup_token)

            if not user.verified:
                user.verified = True
                user.put()

            sign_up_success(self)
            return
        elif verification_type == 'p':
            # supply user to the page
            params = {
                'user': user,
                'token': signup_token
            }
            self.render('resetpassword.html', params)
        else:
            logging.info('verification type not supported')
            self.abort(404)


class SignupHandler(BaseRequestHandler):
    def get(self):
        #valid_id(self)
        #id = self.request.get('ID')
        #print id + "iddddddddddddd"
        #if not cheak_id():
        #     self.display_message('The ID: %s is not valid' % id)
        #     return

        if not user_has_session(self):
            error_message(self, 'We couldn\'t sign you up. Please try again.')

        self.render('signup.html')

    def post(self):
        if not user_has_session(self):
            error_message(self, 'We couldn\'t sign you up. Please try again.')

        user_name = self.request.get('username')
        email = self.request.get('email')
        name = self.request.get('name')
        password = self.request.get('password')
        last_name = self.request.get('lastname')

        unique_properties = ['email_address']
        user_data = self.user_model.create_user(user_name,
                                                unique_properties,
                                                email_address=email, name=name, password_raw=password,
                                                last_name=last_name, verified=False)
        if not user_data[0]: #user_data is a tuple
            self.display_message('Unable to create user for email %s because of \
        duplicate keys %s' % (user_name, user_data[1]))
            return

        user = user_data[1]
        user_id = user.get_id()

        token = self.user_model.create_signup_token(user_id)
        #store the id + connecttion way
        self.session['user_email'] = email #####################################################3
        self.session['connection'] = "self"
        self.session['curr_logged_in'] = True
        self.session['fb_g_o'] = name

        verification_url = self.uri_for('verification', type='v', user_id=user_id, email=email,
                                        signup_token=token, _full=True)

        msg = 'Send an email to user in order to verify their address. \
          They will be able to do so by visiting <a href="{url}">{url}</a>'

        self.display_message(msg.format(url=verification_url))


class AuthenticatedHandler(BaseRequestHandler):
    @user_required
    def get(self):
        self.render('authenticated.html')


class ForgotPasswordHandler(BaseRequestHandler):
    def get(self):
        self._serve_page()

    def post(self):
        username = self.request.get('username')

        user = self.user_model.get_by_auth_id(username)
        if not user:
            logging.info('Could not find any user entry for username %s', username)
            self._serve_page(not_found=True)
            return

        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='p', user_id=user_id,
                                        signup_token=token, _full=True)

        msg = 'Send an email to user in order to reset their password. \
          They will be able to do so by visiting <a href="{url}">{url}</a>'

        self.display_message(msg.format(url=verification_url))

    def _serve_page(self, not_found=False):
        username = self.request.get('username')
        params = {
            'username': username,
            'not_found': not_found
        }
        self.render('forgot.html', params)


class SetPasswordHandler(BaseRequestHandler):
    @user_required
    def post(self):
        password = self.request.get('password')
        old_token = self.request.get('t')

        if not password or password != self.request.get('confirm_password'):
            self.display_message('passwords do not match')
            return

        user = self.user
        user.set_password(password)
        user.put()

        # remove signup token, we don't want users to come back with an old link
        self.user_model.delete_signup_token(user.get_id(), old_token)

        self.display_message('Password updated')

##############################


class SignUpPopUp(BaseRequestHandler):
    def post(self):
        class_key = cgi.escape(self.request.get('class_key')) #works great!
        date_representation = cgi.escape(self.request.get('class_date'))
        date_original = date_representation
        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]
        if not self.logged_in:
            return self.redirect('/authenticated')
            #return self.redirect('/user_auth')

        user_viewer = UserView(self.get_user_id(), class_key, year, month, day)
        course = user_viewer.get_course_by_id()
        code = user_viewer.get_view_code(course)
        signed_up = (code == user_manager.USER_ALREADY_REGISTERED)
        registration_open = (code != user_manager.REGISTRATION_DID_NOT_START)
        time_passed = (code == user_manager.COURSE_TIME_PASSED)
        print time_passed
        if code == user_manager.NO_SUCH_COURSE:
            pass #self.render('user-popup-fail.html')
        else:
            registration_open_date = course.calculate_open_registration_date(year, month, day)
            if registration_open_date is None:
                year = str(0)
                month = str(0)
                day = str(0)
                start_time = str(0)
            else:
                year = str(registration_open_date.year)
                month = str(registration_open_date.month)
                day = str(registration_open_date.day)
                hour = course.registration_start_time[:2]
                minutes = course.registration_start_time[2:]
                start_time = hour + ":" + minutes

            template_values = {
                'course': {
                    'name': course.name,
                    'studio': course.studio,
                    'class_key': course.id,
                    'color': course.color,
                    'free_slots': course.get_num_open_slots(),
                    'start_time': course.hour[:2] + ":" + course.hour[2:],
                    'end_time': get_end_time(long(course.milli), course.duration),
                    'date': date_original,
                    'signed_up': signed_up,
                    'is_registration_open': registration_open,
                    'instructor': course.instructor,
                    'time_passed': time_passed,
                    'registration_year': year,
                    'registration_month': month,
                    'registration_day': day,
                    'registration_hour': start_time
                }
            }
            #template = JINJA_ENVIRONMENT.get_template('user-popup.html')
            #self.response.write(template.render(template_values))
            print year
            print month
            print day
            self.render('user-popup.html', template_values)


class NewCoursePopup(BaseRequestHandler):
    def post(self):
        class_date = cgi.escape(self.request.get('course_date'))
        class_hour = cgi.escape(self.request.get('course_hour'))
        class_minutes = cgi.escape(self.request.get('course_minutes'))
        admin_viewer = AdminViewer("peer", "peer")
        gym_info = admin_viewer.get_gym_info_for_popup()
        class_names = gym_info.courses_template_table
        studio_names = gym_info.studios_list
        instructor_names = gym_info.instructors_table
        template_values = {
            'class_names': class_names,
            'studio_names': studio_names,
            'instructor_names': instructor_names,
            'class_time': class_hour,
            'class_date': class_date,
            'class_minutes': class_minutes
        }
        self.render('admin-new-course.html', template_values)

class EditCourseButtonClick(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        admin_viewer = AdminViewer("peer", "peer")
        gym_info = admin_viewer.get_gym_info_for_popup()
        class_names = gym_info.courses_template_table
        studio_names = gym_info.studios_list
        instructor_names = gym_info.instructors_table
        class_key = cgi.escape(self.request.get('class_id')) #works great!
        date_representation = cgi.escape(self.request.get('class_date'))
        class_hour =  cgi.escape(self.request.get('class_hour'))
        original_date = date_representation
        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]
        registered_users_list = admin_manager.get_registered_users_list_from_course(class_key, year, month, day)
        waiting_list = admin_manager.get_waiting_list_from_course(class_key, year, month, day)
        course = admin_manager.get_course(class_key, year, month, day)
        hour = course.registration_start_time[:2]
        minutes = course.registration_start_time[2:]
        reg_start_time = hour + ":" + minutes
        template_values = {
            'users': registered_users_list,
            'waiting_list': waiting_list,
            'course': course,
            'class_names': class_names,
            'studio_names': studio_names,
            'instructor_names': instructor_names,
            'class_date':original_date,
            'class_hour':class_hour,
            'reg_start_time':reg_start_time
        }
        self.render('admin-edit-course.html', template_values)


class AddClassToSched(BaseRequestHandler):
    def post(self):
        date = cgi.escape(self.request.get('date')).split("/")
        time = cgi.escape(self.request.get('time'))
        length = cgi.escape(self.request.get('length'))
        participants = cgi.escape(self.request.get('participants'))
        class_name = cgi.escape(self.request.get('class'))
        studio = cgi.escape(self.request.get('studio'))
        instructor = cgi.escape(self.request.get('instructor'))
        registration_days_before = int(cgi.escape(self.request.get('open_date')))
        registratio_start_time = cgi.escape(self.request.get('open_time'))
        all_month = cgi.escape(self.request.get('all_month'))
        admin_man = AdminManager("peer", "peer") # todo: gym not hard coded
        if str(all_month) == 'true':
            admin_man.create_course_for_month(class_name, time.replace(":", ""), length, participants, instructor,
                                              studio,
                                              "blue", {}, {}, registration_days_before,
                                              registratio_start_time.replace(":", ""), date[2],
                                              date[1],
                                              admin_man.get_day_by_date(int(date[2]), int(date[1]), int(date[0])))
        else:
            admin_man.create_course_instance(class_name, time.replace(":", ""), length, participants, instructor,
                                             studio,
                                             "blue", {}, {}, registration_days_before,
                                             registratio_start_time.replace(":", ""), date[2],
                                             date[1], date[0])


class EditCoursePopup(BaseRequestHandler):
    def post(self):
        class_id = cgi.escape(self.request.get('class_id'))
        date = cgi.escape(self.request.get('date')).split("/")
        time = cgi.escape(self.request.get('time'))
        length = cgi.escape(self.request.get('length'))
        participants = cgi.escape(self.request.get('participants'))
        class_name = cgi.escape(self.request.get('class'))
        studio = cgi.escape(self.request.get('studio'))
        instructor = cgi.escape(self.request.get('instructor'))
        registration_days_before = int(cgi.escape(self.request.get('open_date')))
        registratio_start_time = cgi.escape(self.request.get('open_time'))
        all_month = cgi.escape(self.request.get('all_month'))
        admin_man = AdminManager("peer", "peer") # todo: gym not hard coded
        admin_man.edit_course(class_id, class_name, length, participants, instructor, studio, registration_days_before,
                              registratio_start_time, date[2], date[1], date[0])


class ManageCoursePopup(BaseRequestHandler):
    def post(self):
        class_key = cgi.escape(self.request.get('class_id'))
        date_representation = cgi.escape(self.request.get('class_date'))

        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]

        admin_manager = AdminManager("peer", "peer") #todo gym not hardcoded
        registered_users_list = admin_manager.get_registered_users_list_from_course(class_key, year, month, day)
        waiting_list = admin_manager.get_waiting_list_from_course(class_key, year, month, day)
        course = admin_manager.get_course(class_key, year, month, day)
        template_values = {
            'users': registered_users_list,
            'waiting_list': waiting_list,
            'course': course

        }
        self.render('admin-manage-course.html', template_values)


class EditCourseTime(BaseRequestHandler):
    def post(self):
        new_date = cgi.escape(self.request.get('new_date'))
        old_date = cgi.escape(self.request.get('old_date'))
        is_same_day = new_date == old_date
        new_date = new_date.split('/')
        old_date = old_date.split('/')
        start_hour = cgi.escape(self.request.get('new_hour')).replace(":", "")
        duration = cgi.escape(self.request.get('new_minutes'))
        course_id = cgi.escape(self.request.get('course_id'))
        admin_manager = AdminManager("peer", "peer") #todo: gym not hard coded
        if is_same_day:
            admin_manager.edit_course_time(course_id, new_date[2], new_date[1], new_date[0], start_hour, duration)
        else:
            admin_manager.edit_course_time_and_day(course_id, old_date[2], old_date[1], old_date[0],
                                                   new_date[2], new_date[1], new_date[0], start_hour, duration)
        course = admin_manager.get_course(course_id, new_date[2], new_date[1], new_date[0])
        template_values = {
            'instructor': course.instructor,
            'open_slots': course.get_num_open_slots()
        }
        self.response.write(jsonpickle.encode(template_values))


class InitialHandler(BaseRequestHandler):
    def get(self):
        """initialize the db"""
        """create gym and put in db:"""
        admin_manager = AdminManager("peer", "peer")
        #admin_manager.create_gym("tel aviv")

        """add month schedule"""

        admin_manager.create_month_schedule(2013, 12)
        admin_manager.create_month_schedule(2013, 11)
        """create DailyScheduleManager"""
        daily_sched_manager = DailyScheduleManager(admin_manager.gym_network, admin_manager.gym_branch)
        #daily_list = daily_sched_manager.get_daily_schedule_list_from_today(3)
        #self.response.write(str(daily_list[0].day_in_week))

        courses_list = ["Core", "Yoga Flow", "האטה יוגה", "יוגילאטיס", "עיצוב דינאמי", "פלנדקרייז", "Core Fit ball",
                        "אימון פונקציונאלי", "התעמלות בונה עצם", "מתיחות", "עיצוב וחיזוק", "קיקבוקס שקים",
                        "מתיחות+ core",
                        "Fight & Burn", "אימון ריצה", "ויניאסה יוגה", "סטריפ דאנס", "פאוור יוגה", "Fight & Learn",
                        "פילאטיס Core",
                        "אשטנגה יוגה", "זומבה", "סמאש קיקבוקס", "פילאטיס", "Shape 'n' Burn", "בטן ישבן ירכיים",
                        "יסודות פונקציונאלי", "אשטנגה ויניאסה יוגה",
                        "יוגה אורבנית", "ספינינג", "פילאטיס מיטות", "יוגה על הבוקר", "פילאטיס דינאמי", "אימון שקים",
                        "שטנגה""", "סמאש", "אימון פונקציונלי", "Power yoga", "Core פיטבול", "עיצוב וחיטוב",
                        "בטן + מתיחות", "Flow yoga", "ויג'ננה יוגה", "פלדנקרייז", "Fight&burn", "רקודי בטן",
                        "Core Fitball", "קוויקי פונקציונלי"]

        for course in courses_list:
            admin_manager.add_course_template(course, "Description")

        """add course templates"""
        #admin_manager.add_course_template("Zumba", "stupid course")
        #admin_manager.add_course_template("Yoga", "ugly course")
        #admin_manager.add_course_template("yoga", "ugly course")
        #admin_manager.add_course_template("יוגה", "stupid course")
        #admin_manager.add_course_template("ויניאסה יוגה", "stupid course")
        #admin_manager.add_course_template("פילאטיס", "stupid course")
        #admin_manager.add_course_template("פילאטיס", "stupid course")
        #admin_manager.add_course_template("התעמלות בונה עצם", "stupid course")
        #admin_manager.add_course_template("עיצוב וחיזוק", "stupid course")
        #admin_manager.add_course_template("זומבה", "stupid course")

        self.response.write(admin_manager.get_courses_templates())

        """add course template"""
        #admin_manager.add_course_template("Zumba", "stupid course")
        #admin_manager.add_course_template("Yoga", "ugly course")
        #admin_manager.add_course_template("yoga", "ugly course") #won't succeed, because Yoga already exist
        #self.response.write(admin_manager.get_courses_templates())

        """add studios"""
        admin_manager.add_studio("סטודיו 1")
        admin_manager.add_studio("סטודיו 2")

        instructors_list = ["קרן סגל", "טל ספורטה", "ורדי פרידמן", "מיכל גליק", "ג'ני בירגר", "לריסה ברגוב",
                            "שיראל שלוש", "מעין דהרי", "איילת צפריר", "מיה תדהר", "חן סבן", "אדוה אופיר",
                            "רוני קלע", "מיכל לוי", "קרן אור קיצ'ס", "ליאת קמחי", "מרחב מוהר", "גיא אלון",
                            "גלית גל", "דין ירושלמי", "שי עובדיה", "יפעת פילוסוף", "רותם שמילוביץ", "נעמה שחר",
                            "יעל אזולאי", "ארז אפון", "יעל לילה", "בני שוורץ"]

        """ add instructor """
        i = 1
        for instuctor in instructors_list:
            instructor_arr = instuctor.split(" ")
            first_name = instructor_arr[0]
            last_name = instructor_arr[1]
            admin_manager.add_instructor(i, first_name, last_name)
            i += 1

        """create courses"""

        admin_manager.create_course_for_month("יוגה על הבוקר", "0800", 60, 10,
                                              "קרן סגל", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("פילאטיס", "0900", 60, 20,
                                              "מעין דהרי", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("עיצוב וחיזוק", "1100", 60, 20,
                                              "לריסה בגוב", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("אשטנגה יוגה", "1100", 60, 25,
                                              "מיכל לוי", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("פילאטיס דינאמי", "1745", 60, 25,
                                              "אדוה אופיר", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("עיצוב וחיזוק", "1830", 60, 25,
                                              "מעין דהרי", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("זומבה", "1930", 60, 25,
                                              "רותם שמילוביץ", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("שטנגה", "2000", 90, 25,
                                              "יעל אזולאי", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("אימון שקים", "2030", 60, 20,
                                              "שי עובדיה", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              1)
        admin_manager.create_course_for_month("ויניאסה יוגה", "0800", 60, 20,
                                              "טל ספורטה", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("פילאטיס", "0800", 60, 20,
                                              "מיכל גליק", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("עיצוב דינאמי", "1000", 60, 20,
                                              "מיה תדהר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("Core פיטבול", "1100", 60, 20,
                                              "אדוה אופיר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("Power yoga", "1730", 60, 20,
                                              "דין ירושלמי", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("אימון פונקציונלי", "1745", 60, 20,
                                              "גיא אלון", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("סמאש", "1830", 60, 20,
                                              "שי עובדיה", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("עיצוב וחיטוב", "1930", 60, 20,
                                              "לריסה בגוב", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("פילאטיס", "2000", 60, 20,
                                              "שיראל שלוש", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("זומבה", "2030", 60, 20,
                                              "רוני קלע", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              2)
        admin_manager.create_course_for_month("יוגה על הבוקר", "0830", 60, 20,
                                              "ורדי פרידמן", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              3)

        admin_manager.create_course_for_month("בטן + מתיחות", "0800", 60, 20,
                                              "ג'ני בירגר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              3)

        admin_manager.create_course_for_month("פלדנקרייז", "0900", 60, 20,
                                              "איילת צפריר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              3)
        admin_manager.create_course_for_month("פילאטיס", "1000", 60, 20,
                                              "מיכל גליק", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              3)
        admin_manager.create_course_for_month("ויג'ננה יוגה", "1645", 60, 15,
                                              "גלית גל", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              3)
        admin_manager.create_course_for_month("בטן ישבן ירכיים", "1800", 60, 12,
                                              "יפעת פילוסוף", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              3)
        #admin_manager.create_course_for_month("Flow yoga", "1845", 60, 20,
        #                                      "ליאת קימחי", "1", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      3)
        #admin_manager.create_course_for_month("פילאטיס", "1900", 60, 20,
        #                                      "חן סבן", "1", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      3)
        #admin_manager.create_course_for_month("בטן + מתיחות", "2000", 60, 20,
        #                                      "ארז אפון", "1", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      3)
        #admin_manager.create_course_for_month("Fight&burn", "2000", 60, 15,
        #                                      "מרחב מוהר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      3)
        admin_manager.create_course_for_month("Core Fitball", "1845", 60, 15,
                                              "לריסה בגוב", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        admin_manager.create_course_for_month("פילאטיס", "0900", 60, 20,
                                              "לריסה בגוב", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        admin_manager.create_course_for_month("התעמלות בונה עצם", "1000", 60, 20,
                                              "מיה תדהר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        admin_manager.create_course_for_month("אשטנגה יוגה", "1100", 60, 20,
                                              "מיכל לוי", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        admin_manager.create_course_for_month("Power yoga", "1745", 60, 20,
                                              "גיא אלון", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        #admin_manager.create_course_for_month("אימון פונקציונלי", "1830", 60, 15,
        #                                      "מרחב מוהר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      4)
        #admin_manager.create_course_for_month("סמאש", "1930", 60, 20,
        #                                      "נעמה שחר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      4)
        #admin_manager.create_course_for_month("פילאטיס", "1900", 60, 20,
        #                                      "שיראל שלוש", "1", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      4)
        admin_manager.create_course_for_month("רקודי בטן", "2000", 60, 20,
                                              "יעל לילה", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        admin_manager.create_course_for_month("אימון ריצה", "2000", 60, 20,
                                              "בני שוורץ", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        admin_manager.create_course_for_month("עיצוב וחיזוק", "2000", 60, 20,
                                              "ארז אפון", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        admin_manager.create_course_for_month("זומבה", "2130", 60, 20,
                                              "רוני קלע", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              4)
        admin_manager.create_course_for_month("ויניאסה יוגה", "0800", 60, 20,
                                              "טל ספורטה", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              5)
        admin_manager.create_course_for_month("פילאטיס", "0800", 60, 16,
                                              "שיראל שלוש", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              5)
        admin_manager.create_course_for_month("פלדנקרייז", "0900", 60, 20,
                                              "איילת צפריר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              5)
        admin_manager.create_course_for_month("עיצוב דינאמי", "1000", 60, 18,
                                              "מיה תדהר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              5)
        admin_manager.create_course_for_month("פילאטיס דינאמי", "1100", 60, 20,
                                              "אדוה אופיר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              5)
        admin_manager.create_course_for_month("בטן ישבן ירכיים", "1800", 60, 20,
                                              "יפעת פילוסוף", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              5)
        admin_manager.create_course_for_month("פאוור יוגה", "1830", 60, 18,
                                              "גיא אלון", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              5)
        #admin_manager.create_course_for_month("עיצוב וחיזוק", "1900", 60, 20,
        #                                      "לריסה בגוב", "2", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      5)
        #admin_manager.create_course_for_month("קוויקי פונקציונלי", "1900", 60, 20,
        #                                      "דין ירושלמי", "1", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      5)
        #admin_manager.create_course_for_month("קוויקי פונקציונלי", "1930", 60, 20,
        #                                      "דין ירושלמי", "1", "blue", {}, {}, "5", "1000", 2013, 12,
        #                                      5)

        admin_manager.create_course_for_month("יוגה על הבוקר", "0845", 60, 25,
                                              "ורדי פרידמן", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              6)
        admin_manager.create_course_for_month("פילאטיס Core", "1000", 60, 25,
                                              "חן סבן", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              6)
        admin_manager.create_course_for_month("זומבה", "1100", 60, 20,
                                              "רוני קלע", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              6)
        admin_manager.create_course_for_month("אשטנגה ויניאסה יוגה", "1215", 60, 20,
                                              "קרו אור קיצ'ס", "1", "blue", {}, {}, "5", "1000", 2013, 12,
                                              6)
        admin_manager.create_course_for_month("עיצוב וחיזוק", "1200", 60, 20,
                                              "מיה תדהר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              6)
        admin_manager.create_course_for_month("FIGHT&BURN", "1300", 60, 20,
                                              "מרחב מוהר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              6)
        admin_manager.create_course_for_month("עיצוב וחיזוק", "1100", 60, 20,
                                              "לריסה בגוב", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              7)
        admin_manager.create_course_for_month("Flow yoga", "1215", 60, 20,
                                              "ליאת קימחי", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              7)
        admin_manager.create_course_for_month("מתיחות+ core", "1230", 60, 20,
                                              "שיראל שלוש/לריסה בגוב", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              7)
        admin_manager.create_course_for_month("אימון פונקציונלי", "1830", 60, 25,
                                              "מרחב מוהר", "2", "blue", {}, {}, "5", "1000", 2013, 12,
                                              7)

        admin_manager.add_user_to_gym("1", "David", "Franco", "Fdas", "43242")
        admin_manager.add_user_to_gym("2", "Roy", "Klinger", "Fdas", "4324fda3242")
        admin_manager.add_user_to_gym("3", "Moshe", "Rumba", "Fdas", "4324fda")
        admin_manager.add_user_to_gym("123", "Moshe", "Rumba", "Fdas", "4324fda")
        admin_manager.add_user_to_gym("555", "Moshe", "Rumba", "Fdas", "4324fda")

        user_credential = entities.UserCredentials()
        user_credential.id = '1'
        user_credential.gym_branch = 'peer'
        user_credential.gym_network = 'peer'
        user_credential.set_key()
        user_credential.put()

        user_credential = entities.UserCredentials()
        user_credential.id = '2'
        user_credential.gym_branch = 'peer'
        user_credential.gym_network = 'peer'
        user_credential.set_key()
        user_credential.put()

        user_credential = entities.UserCredentials()
        user_credential.id = '3'
        user_credential.gym_branch = 'peer'
        user_credential.gym_network = 'peer'
        user_credential.set_key()
        user_credential.put()

        user_credential = entities.UserCredentials()
        user_credential.id = '123'
        user_credential.gym_branch = 'peer'
        user_credential.gym_network = 'peer'
        user_credential.set_key()
        user_credential.put()
        #user 2
        user_credential = entities.UserCredentials()
        user_credential.id = '555'
        user_credential.gym_branch = 'peer'
        user_credential.gym_network = 'peer'
        user_credential.set_key()
        user_credential.put()
        #self.response.write(str(daily_list[0].courses_list[0].name))


class AddUser(BaseRequestHandler):
    def get(self):
        david = entities.UserCredentials(id="3213908", gym_network="peer", gym_branch="peer", google_id="3241",
                                         facebook_id="4124321")
        david.set_key()
        david.put()

        admin_man = AdminManager("peer", "peer")
        admin_man.add_user_to_gym('555', "Roy", "Klinger", "fadkj@fdas.fds", "05421365648")
        admin_man.add_user_to_gym('123', "Moahe", "Babi", "ffdskj@fdas.fds", "0546855648")
        admin_man.add_user_to_gym("1", "David", "Franco", "Fdas", "43242")
        admin_man.add_user_to_gym("2", "Roy", "Klinger", "Fdas", "4324fda3242")
        admin_man.add_user_to_gym("3", "Moshe", "Rumba", "Fdas", "4324fda")
        admin_man.add_user_to_gym("4252", "oimdas", "Rmdkam", "Fdas", "4324fda")

        self.response.write("Hey")


class MainHandler(BaseRequestHandler):
    def get(self):
        admin_manager = AdminManager("peer", "peer")



        ## add

        #admin_manager.add_instructor("123456", "Roy", "Klinger")
        #admin_manager.add_instructor("1234326", "Moshe", "Tuki")
        #admin_manager.add_studio("Spinning Room")
        #admin_manager.add_studio("Yoga Room")
        #

        #
        #hour = datetime.now().hour
        #
        #admin_manager.create_course_for_month("ZumbaLatis", "Latis the Zumbot","1400", 120, 10,
        #                      "Moished", "Park","blue", [], [], 2013, 11, 3)
        #
        #
        #admin_manager.create_course_for_month("PilaYoga", "Yoga the Pila", "0930", 60, 10,
        #                      "Moished", "Park","blue", [], [], 2013, 11, 5)

        ###############################

        #peer = entities.Gym(name="peer", gym_network="peer", address="TLV", courses={}, instructors={}, studios=[])
        #peer.set_key()
        #peer.put()

        #creating course templates
        #zumba = objects.CourseTemplate("Zumba", "Funny course")
        #yoga = objects.CourseTemplate("Yoga", "Stupid course")

        # creating gyms

        #goactive = entities.Gym(name = "savyonim",gym_network="Go Active")

        #goactive.set_key()

        # uploading gyms to DB
        #goactive.put()


        #
        #admin = AdminManager("peer", "peer")
        #admin.add_course_template("yoga", "Zubin Meta")
        #admin.create_month_schedule(2014, 2)
        ##admin.edit_course_template("yoga","yoga11","Kaki batachton!")
        #admin.create_course_for_month("ZumbaLatis", "Latis the Zumbot", hour, 120, 10,
        #                              "Moished", "Park","blue", [], [], 2014, 2, 3)
        #day_number = admin.get_day_by_date(2013, 11, 7)
        #
        ## add user to zumbalatis
        #daily_sched_man = operations.DailyScheduleManager("peer", "peer")
        #daily_sched_man.add_user_to_course("Roy Klinger", 2014, 2, 3, hour, "ZumbaLatis")
        #daily_sched_man.add_user_to_course("Moshico Movshi", 2014, 2, 3, hour, "ZumbaLatis")
        #
        #daily = entities.MonthSchedule.get_key(2, 2014, "peer", "peer").get().schedule_table[str(3)]
        #for course in daily.courses_list:
        #    if course.name == "ZumbaLatis":
        #        self.response.write("before deletion: <br/>")
        #        for user in course.users_list:
        #            self.response.write("his name is: " + user.name + "<br/>")
        #
        #daily_sched_man.delete_user_from_course("Moshico Movshi", 2014, 2, 3, hour, "ZumbaLatis")
        #
        #daily1 = entities.MonthSchedule.get_key(2, 2014, "peer", "peer").get().schedule_table[str(3)]
        #for course in daily1.courses_list:
        #    if course.name == "ZumbaLatis":
        #        self.response.write("after deletion: <br/>")
        #        for user in course.users_list:
        #            self.response.write("his name is: " + user.name + "<br/>")
        #
        #peer_gym_after = entities.Gym.get_key("peer", "peer").get()
        #course_templates = peer_gym_after.courses
        #schedule = entities.MonthSchedule.get_key(2, 2014, "peer", "peer").get()
        #self.response.write(str(course_templates) + "<br/>")
        #self.response.write(str(schedule.schedule_table.keys()) + "<br/>")
        #self.response.write(str(schedule.schedule_table['3'].courses_list) + "<br/>")
        #self.response.write(str(day_number) + "<br/>")
        #
        ## creating real courses
        #zumba_yaron = objects.Course("Zumba", "Funny course", 1400, 60, 20, "yaron","Katom", "#FF99FF", [],[])
        #yoga_bar = objects.Course("Yoga", "Stupid course", 1700, 90, 90, "yaron", "blue", "#3399FF",[], [])
        #
        #
        ## creating schedule
        #schedule_peer = entities.MonthSchedule()
        #schedule_peer.month = 11
        #schedule_peer.year = 2013
        #schedule_peer.set_key("peer", "peer")
        #first_day = objects.DailySchedule(2013, 11, 1, 3, [zumba_yaron, yoga_bar])
        #second_day = objects.DailySchedule(2013, 11, 2, 5, [zumba_yaron, yoga_bar])
        #schedule_peer.schedule_table = {int(first_day.day_in_month): first_day, int(second_day.day_in_month): second_day}
        #
        #schedule_sav = entities.MonthSchedule()
        #schedule_sav.month = 7
        #schedule_sav.year = 2011
        #schedule_sav.set_key("Go Active", "savyonim")
        #
        #schedule_sav.put()
        #schedule_peer.put()
        #
        ##create users
        #david = objects.User(12342156, 3, 144221, "david")
        #matan = objects.User(12323126, 2, 1321, "matan")
        #omri = objects.User(123756456, 1, 1321, "omri")
        #roy = objects.User(123432356, 4, 1321, "roy")
        #
        #users = entities.Users()
        #users.set_key("peer", "peer")
        #users.users_table = users.create_users_table(david, matan, omri, roy)
        #users.put()
        #
        #users_manager = operations.DailyScheduleManager("peer", "peer")
        #start_date = datetime(day=1, month=11, year=2013)
        #end_date = datetime(day=2, month=11, year=2013)
        #
        #result = entities.MonthSchedule.get_key("11","2013","peer","peer").get()
        #if type(result.schedule_table[str(first_day.day_in_month)]) == objects.DailySchedule:
        #    self.response.write("I'm Daily Sche........!!" + "<br/>")
        #self.response.write(str(result.schedule_table[str(first_day.day_in_month)].day_in_month) + "<br/>")
        #self.response.write(str(users_manager.get_daily_schedule_list(start_date, end_date)[0].courses_list[0].studio))


class ChangeWeek(BaseRequestHandler):
    def post(self):
        users_manager = DailyScheduleManager("peer", "peer")
        gym_manager = GymManager("peer", "peer")
        admin_manager = AdminManager("peer", "peer")
        client_date = float(cgi.escape(self.request.get('new_date')))
        new_date = datetime.fromtimestamp(client_date / 1e3) + timedelta(hours = 2)
        print new_date
        sched = admin_manager.get_weekly_daily_schedule_list_by_date(new_date)

        self.response.write(jsonpickle.encode(sched))


class UserHandler(BaseRequestHandler):
    def get(self):
        template_values = {
            'logged_in': self.logged_in,
            'user': self.user
            #'mili_times': mili_times
        }

        self.render('user_grid.html', template_values)


class AdminHandler(BaseRequestHandler):
    def get(self):
        #template = JINJA_ENVIRONMENT.get_template('admin_grid.html')
        #self.response.write(template.render())
        admin_manager = AdminManager("peer", "peer")
        gym_users = admin_manager.gym.users_table
        instructors = admin_manager.gym.instructors
        courses_templates = admin_manager.gym.courses
        studios = admin_manager.gym.studios
        template_values = {
            'users':gym_users,
            'instructor_names':instructors,
            'courses':courses_templates,
            'studios':studios
        }

        self.render('admin_grid.html', template_values)


class CreateMonthSched(BaseRequestHandler):
    def post(self):
        full_date = cgi.escape(self.request.get('month'))
        date_arr = full_date.split('-')
        year = date_arr[0]
        month = date_arr[1]
        #self.response.write(date_arr)
        admin_man = AdminManager("peer", "peer")
        admin_man.create_month_schedule(int(year), int(month))

        template_values = {
            'year': year,
            'month': month,
            'courses': admin_man.get_courses_templates(),
            'instructors': admin_man.get_instructors(),
            'studios': admin_man.get_studios()
        }
        #template = JINJA_ENVIRONMENT.get_template('create_monthly_schedule.html')
        #self.response.write(template.render(template_values))
        self.render('create_monthly_schedule.html', template_values)


class CreateMonthYear(BaseRequestHandler):
    def get(self):
        template_values = {

        }
        #template = JINJA_ENVIRONMENT.get_template('choose_month_year.html')
        #self.response.write(template.render(template_values))
        self.render('choose_month_year.html', template_values)


class AddCourse(BaseRequestHandler):
    def post(self):
        course_name = cgi.escape(self.request.get('course_name'))
        description = cgi.escape(self.request.get('description'))

        admin_man = AdminManager("peer", "peer")
        admin_man.add_course_template(course_name, description)

        template_values = {
            'year': self.request.get('year'),
            'month': self.request.get('month'),
            'courses': admin_man.get_courses_templates()
        }

        #template = JINJA_ENVIRONMENT.get_template('create_monthly_schedule.html')
        #self.response.write(template.render(template_values))
        self.render('create_monthly_schedule.html', template_values)


class CreateCourse(BaseRequestHandler):
    def post(self):
        year = cgi.escape(self.request.get('year'))
        month = cgi.escape(self.request.get('month'))
        day = cgi.escape(self.request.get('day'))
        class_name = cgi.escape(self.request.get('classes'))
        studio = cgi.escape(self.request.get('studio'))
        instructor = cgi.escape(self.request.get('instructor'))
        start_hour = cgi.escape(self.request.get('start_hour')).replace(":", "")
        duration = cgi.escape(self.request.get('duration'))
        capacity = cgi.escape(self.request.get('capacity'))

        schedule_man = DailyScheduleManager("peer", "peer")

        #print("year = "+year + " month= "+ month+ " class= " + str(class_name) + " studio= "+
        #             studio + " instructor= " + instructor + " start= " + start_hour +
        #                 " duration= " + duration + " capacity= " + capacity + " day= " + day)

        # Get description
        admin_man = AdminManager("peer", "peer")
        class_template = admin_man.get_courses_templates()[str(class_name)]
        description = class_template.description
        # Add course

        admin_man.create_course_for_month(class_name, description, start_hour, duration, capacity, instructor
            , studio, "lavenderblush", [], [], year, month, day)
        # Get signed courses

        today = date(int(year), int(month), 1)
        in_a_week = date(int(year), int(month), 7)
        daily_scheduale_list = schedule_man.get_daily_schedule_list(today, in_a_week)
        singed_courses = self.get_courses_list_from_daily_schedual_list(daily_scheduale_list)
        #self.response.write("year = "+year + " month= "+ month+ " class= " + str(class_name) + " studio= "+
        #                     studio + " instructor= " + instructor + " start= " + start_hour +
        #                         " end= " + end_hour + " capacity= " + capacity +"courses list= " + str(courses))
        template_values = {
            'year': year,
            'month': month,
            'courses': admin_man.get_courses_templates(),
            'singed_courses': singed_courses
        }

        #template = JINJA_ENVIRONMENT.get_template('create_monthly_schedule.html')
        #self.response.write(template.render(template_values))
        self.render('create_monthly_schedule.html', template_values)

    def get_courses_list_from_daily_schedual_list(self, daily_schedual_list):
        result = []
        for daily in daily_schedual_list:
            result.extend(daily.courses_list)
        return result


class RemoveUserFromClass(BaseRequestHandler):
    def post(self):
        class_key = cgi.escape(self.request.get('class_key')) #works great!
        date_representation = cgi.escape(self.request.get('class_date'))

        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]

        if not self.logged_in:
            return self.redirect('/authenticated')

        user_course_manager = UserBusinessLogic(self.get_user_id(), class_key, year, month, day)
        code = user_course_manager.cancel_course_registration()
        if code == user_manager.USER_REMOVED_FROM_COURSE_SUCCEEDED:
            user_view = UserView(self.get_user_id(), class_key, year, month, day)
            new_num_slots_in_course = user_view.get_num_open_slots()

            self.response.write(new_num_slots_in_course);


class RegisterToClass(BaseRequestHandler):
    def post(self):
        class_key = cgi.escape(self.request.get('class_key')) #works great!
        date_representation = cgi.escape(self.request.get('class_date'))
        date_original = date_representation
        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]

        if not self.logged_in:
            return self.redirect('/authenticated')

        user_course_manager = UserBusinessLogic(self.get_user_id(), class_key, year, month, day)
        code = user_course_manager.register_to_course()
        if code == user_manager.USER_REGISTRATION_SUCCEEDED:
            user_view = UserView(self.get_user_id(), class_key, year, month, day)
            new_num_slots_in_course = user_view.get_num_open_slots()
            course = user_course_manager.get_course_by_id()
            course_name = course.name
            course_start_hour = course.hour[:2] + ":" + course.hour[2:]
            course_end_hour = get_end_time(long(course.milli), course.duration)


            template_values = {
                'open_slots': new_num_slots_in_course,
                'class_key': class_key,
                'date': date_original,
                'name':course_name,
                'start_hour':course_start_hour,
                'end_hour':course_end_hour

            }

            self.render('user-popup-success.html', template_values)
        else:
            template_values = {
                'error_code': code
            }
            self.render('user-popup-fail.html', template_values)


class GetUsersList(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        users_table = admin_manager.get_users_of_gym()
        self.response.write(jsonpickle.encode(users_table))


class AddUserToCourse(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        class_id = cgi.escape(self.request.get('class_id')) #works great!
        date_representation = cgi.escape(self.request.get('class_date'))
        user_id = cgi.escape(self.request.get('user_id'))

        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]

        code = admin_manager.add_user_to_course(class_id, user_id, year, month, day)
        if code == user_manager.USER_REGISTRATION_SUCCEEDED:
            user_view = UserView(user_id, class_id, year, month, day)
            new_num_slots_in_course = user_view.get_num_open_slots()
            template_values = {
                'open_slots': new_num_slots_in_course,
                'class_key': class_id
            }
            self.response.write(jsonpickle.encode(template_values));


class RemoveUserFromCourse(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        class_key = cgi.escape(self.request.get('class_id')) #works great!
        date_representation = cgi.escape(self.request.get('class_date'))
        user_id = cgi.escape(self.request.get('user_id'))

        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]

        admin_manager.delete_user_from_course(class_key, user_id, year, month, day)
        user_view = UserView(user_id, class_key, year, month, day)
        new_num_slots_in_course = user_view.get_num_open_slots()
        template_values = {
            'open_slots': new_num_slots_in_course,
            'class_key': class_key
        }
        self.response.write(jsonpickle.encode(template_values));


class DeleteCourse(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        class_key = cgi.escape(self.request.get('class_id')) #works great!
        date_representation = cgi.escape(self.request.get('class_date'))
        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]

        admin_manager.delete_course_instance(class_key, year, month, day)

class AddInstructorToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        id = cgi.escape(self.request.get('id'))
        first_name = cgi.escape(self.request.get('first_name'))
        last_name = cgi.escape(self.request.get('last_name'))
        admin_manager.add_instructor(id, first_name, last_name)

class EditInstructorToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        id = cgi.escape(self.request.get('id'))
        first_name = cgi.escape(self.request.get('first_name'))
        last_name = cgi.escape(self.request.get('last_name'))
        admin_manager.edit_instructor(id, first_name,last_name)

class DeleteInstructorToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        id = cgi.escape(self.request.get('instructor_id'))
        admin_manager.delete_instructor(id)


class AddCourseTemplateToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        name = cgi.escape(self.request.get('name'))
        description = cgi.escape(self.request.get('description'))
        color = cgi.escape(self.request.get('color'))
        admin_manager.add_course_template(name, description, color)

class EditCourseTemplateToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        prev_name = cgi.escape(self.request.get('prev_name'))
        new_name = cgi.escape(self.request.get('new_name'))
        new_description = cgi.escape(self.request.get('new_description'))
        new_color = cgi.escape(self.request.get('new_color'))
        admin_manager.edit_course_template(prev_name, new_name, new_description, new_color)

class DeleteCourseTemplateToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        name = cgi.escape(self.request.get('name'))
        admin_manager.delete_course_template(name)

class AddUserToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        user_id = cgi.escape(self.request.get('user_id'))
        first_name = cgi.escape(self.request.get('first_name'))
        last_name = cgi.escape(self.request.get('last_name'))
        email = cgi.escape(self.request.get('email'))
        phone = cgi.escape(self.request.get('phone'))
        admin_manager.add_user_to_gym(user_id, first_name, last_name, email, phone)

class EditUserToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        user_id = cgi.escape(self.request.get('user_id'))
        first_name = cgi.escape(self.request.get('first_name'))
        last_name = cgi.escape(self.request.get('last_name'))
        email = cgi.escape(self.request.get('email'))
        phone = cgi.escape(self.request.get('phone'))
        admin_manager.edit_user(user_id, first_name, last_name, email, phone)

class DeleteUserToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        user_id = cgi.escape(self.request.get('user_id'))
        admin_manager.delete_user_from_gym(user_id)

class AddStudioToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        name = cgi.escape(self.request.get('name'))
        admin_manager.add_studio(name)


class EditStudioToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        old_name = cgi.escape(self.request.get('old_name'))
        new_name = cgi.escape(self.request.get('new_name'))
        admin_manager.edit_studio(old_name, new_name)


class DeleteStudioToGym(BaseRequestHandler):
    def post(self):
        admin_manager = AdminManager("peer", "peer")
        name = cgi.escape(self.request.get('studio_name'))
        admin_manager.delete_studio(name)



#todo consider make users a property in gym
#todo consider make each user an entity instead of users_table


#Help functions

sys.path.insert(0, 'libs')
import jsonpickle

#JINJA_ENVIRONMENT = jinja2.Environment(
#    loader=jinja2.FileSystemLoader('templates'),
#    extensions=['jinja2.ext.autoescape'],
#    autoescape=True)

DEFAULT_GYM_NAME = "default_gym"
DEFAULT_MONTH_YEAR = "01-2001"


def to_mili(day, course):
    return time.mktime(datetime(int(day.year), int(day.month), int(day.day_in_month), int(course.hour[:2]),
                                int(course.hour[2:4]))) * 1000


def create_course_milli_from_daily_schedule_list(daily_sched_list):
    dict = {}
    for daily_sched in daily_sched_list:
        for course in daily_sched.courses_list:
            dict[str(course.id)] = daily_sched.javascript_course_start_datetime(course)
    return dict


def parse_course(str):
    return str.split('_')


def get_end_time(start_time_in_milli, duration_in_minutes):
    end_date_time = datetime.fromtimestamp(start_time_in_milli / 1000.0) + timedelta(0, 0, 0, 0,
                                                                                     int(duration_in_minutes), 2)
    add_zero_befor_minute = len(str(end_date_time.minute)) == 1
    add_zero_befor_hour = len(str(end_date_time.hour)) == 1

    end_time = ""

    if add_zero_befor_hour:
        end_time += "0" + str(end_date_time.hour)
    else:
        end_time += str(end_date_time.hour)

    if add_zero_befor_minute:
        end_time += ":0" + str(end_date_time.minute)
    else:
        end_time += ":" + str(end_date_time.minute)

    return end_time


"""session functions"""


def valid_id(id):
    user = entities.UserCredentials.get_user_entity(id)

    if user is None:
        #arg.display_message('The ID: %s is not valid' % id)
        return False
    else:
        return True


def sign_up_success(param_self):
    #connect user id with fb_g_o id in tables UserCredentials
    user_id = param_self.session.get('curr_user_id')
    fb_g_o = param_self.session.get('fb_g_o')
    user_credentials_from_db = entities.UserCredentials.get_user_entity(user_id)
    connection = param_self.session.get('connection')
    gym_network = user_credentials_from_db.gym_network
    gym_branch = user_credentials_from_db.gym_branch
    user_email = param_self.session.get('user_email')


    #email update
    admin_manager = AdminManager(gym_network, gym_branch)
    users_table = admin_manager.get_users_of_gym()


    curr_user = users_table[user_id]
    #remove the not
    if curr_user.email is not None:
        curr_user.email = user_email

    admin_manager.set_gym()

    print admin_manager.get_users_of_gym()['555'].email
    if connection == 'facebook':

        user_credentials_from_db.facebook_id = fb_g_o
        facebook_user_from_db = entities.FacebookCredentials()
        facebook_user_from_db.user_id = user_id
        facebook_user_from_db.facebook_id = fb_g_o
        facebook_user_from_db.set_key()
        facebook_user_from_db.put()
    elif connection == 'google':
        user_credentials_from_db.google_id = fb_g_o
        google_user_from_db = entities.GoogleCredentials()
        google_user_from_db.user_id = user_id
        google_user_from_db.google_id = fb_g_o
        google_user_from_db.set_key()
        google_user_from_db.put()
    elif connection == 'self':
        user_credentials_from_db.email_id = fb_g_o
        email_user_from_db = entities.EmailCredentials()
        email_user_from_db.user_id = user_id
        email_user_from_db.email_id = fb_g_o
        email_user_from_db.set_key()
        email_user_from_db.put()

    user_credentials_from_db.put()
    param_self.session['on_sign_up'] = False
    param_self.session['curr_logged_in'] = True
    param_self.session['user_email'] = None

    #param_self.render('signup_success.html', {
    #    'user': param_self.current_user,
    #    'session': param_self.auth.get_user_by_session()})

    param_self.redirect('/user')


def user_has_session(param_self):
    try:
        user_id = param_self.session['curr_user_id']
        print user_id
    except:
        return False
    return True


def check_sign_in(self_param):
    try:
        connection = self_param.session.get('connection')
        fb_g_o = self_param.session.get('fb_g_o')
        #entities.UserCredentials.get_user_entity(fb_g_o)
        #need to add self_credentials for email recognition
        #self_param.session['logged_in'] = False
        if connection == 'self':
            email_user = entities.EmailCredentials.get_key(fb_g_o).get()
            user_id = email_user.user_id
            self_param.session['curr_user_id'] = user_id
            self_param.session['curr_logged_in'] = True
            self_param.redirect('/user')
        elif connection == 'facebook':
            facebook_user = entities.FacebookCredentials.get_key(fb_g_o).get()
            user_id = facebook_user.user_id
            self_param.session['curr_user_id'] = user_id
            self_param.session['curr_logged_in'] = True
            self_param.redirect('/user')
        elif connection == 'google':
            google_user = entities.GoogleCredentials.get_key(fb_g_o).get()
            user_id = google_user.user_id
            self_param.session['curr_user_id'] = user_id
            self_param.session['curr_logged_in'] = True
            self_param.redirect('/user')
        else:


            error_message(self_param, 'We couldn\'t log you in. Please check your credentials and try again.')
    except:

        error_message(self_param, 'We couldn\'t log you in. Please check your credentials and try again.')


def error_message(self_param, message, param_self=None):
    self_param.session['on_sign_up'] = False
    self_param.session['connection'] = None
    self_param.session['fb_g_o'] = None
    self_param.session['curr_logged_in'] = False
    self_param.session['user_email'] = None
    self_param.display_message(message)
    return


def my_logout(param_self):
    param_self.session['curr_user_id'] = None
    #param_self.session['user_id'] = None
    param_self.session['fb_g_o'] = None
    param_self.session['curr_logged_in'] = False
    param_self.session['connection'] = None
    param_self.session['user_email'] = None
    #param_self.session_store.set_secure_cookie('_simpleauth_sess', None)
    #param_self.session.cookie_name.maxAge = 0
    #param_self.response.unset_cookie('auth')
    #auth.default_config['max_age'] = 0
    #delete_cookie(key, path=’/’, domain=None)
    param_self.response.headers.add_header('Set-Cookie',
                                           'name=_simpleauth_sess; expires="Fri, 31-Dec-1954 23:59:59 GMT"')
    #param_self.redirect('https://www.facebook.com/logout.php?next=localhost:8080&access_token=USER_ACCESS_TOKEN')
    #param_self.redirect("http://www.facebook.com/logout.php?api_key={0}&;session_key={1}")
    #param_self.redirect('http://m.facebook.com/logout.php?confirm=1&next=http://localhost:8080.com;')



#//////////////////////////////////////////////////////////

class CreateEventHandler(MyCalendar):

    def get(self):
        gym_name = "Pure Gym"
        course_name = cgi.escape(self.request.get('course_name'))
        date_representation = cgi.escape(self.request.get('course_date'))
        date_representation = date_representation.split('/')
        year = date_representation[2]
        month = date_representation[1]
        day = date_representation[0]
        start_hour = cgi.escape(self.request.get('start_hour'))
        end_hour = cgi.escape(self.request.get('end_hour'))

        self.update_calendar(gym_name, course_name, day, month, year, start_hour, end_hour)

        self.update_calendar("Pure Gym" , "Zoombalatis", "10","1","2014","17:00", "18:00")
        #self.update_calendar(self.gym_name , self.course_name, self.day,self.month,self.year,self.start_time, self.end_time)
        print "omrormoemrwoermwoermwoermoermwoermwoermwoer"