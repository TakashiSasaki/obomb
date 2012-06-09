'''
Created on 2012/01/03

@author: Takashi SASAKI
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from gaesessions import get_current_session
from models import SessionKind
import os, uuid
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models.ObombUserKind import ObombUserKind

class LoginGoogle(webapp.RequestHandler):
    def get(self):
        current_session = get_current_session()
        if current_session.get(SessionKind.SESSION_ID_KEY) is None:
            current_session[SessionKind.SESSION_ID_KEY] = uuid.uuid1().get_hex()
        session_id = current_session.get(SessionKind.SESSION_ID_KEY)

        session_kind_gql = SessionKind.SessionKind.gql("WHERE sessionId = :1", [session_id])
        session_entity = session_kind_gql.get()
        if session_entity is not None:
            session_entity = SessionKind()
            session_entity.sessionId = session_id
            session_entity.put()
            
        current_user = users.get_current_user()
        if current_user is not None:
            google_user_identifier = current_user.user_id()
            google_user_nickname = current_user.nickname()
            google_user_email = current_user.email()
            obomb_user_kind_gql = ObombUserKind.gql("WHERE googleUserIdentifier = :1", [current_user.user_id()])
            obomb_user_entities = obomb_user_kind_gql.fetch(1000)
            number_of_obomb_user_entities = len(obomb_user_entities) 
            if number_of_obomb_user_entities == 0:
                obomb_user_entity = ObombUserKind()
                obomb_user_entity.googleUserIdentifier = current_user.user_id()
                obomb_user_entity.put()
                obomb_user_entities = [obomb_user_entity]
        else:
            number_of_obomb_user_entities = 0
            google_user_identifier = None
            google_user_nickname = None
            google_user_email = None

        template_values = {
            'session_id' : current_session.get(SessionKind.SESSION_ID_KEY),
            'google_login_url' : users.create_login_url("/login/google"),
            'google_logout_url' : users.create_logout_url("/login/google"),
            'google_user_nickname' : google_user_nickname,
            'google_user_email' : google_user_email,
            'google_user_identifier': google_user_identifier,
            'number_of_obomb_user_entities': number_of_obomb_user_entities
            }
        path = os.path.join(os.path.dirname(__file__), 'google.djhtml')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        self.get()

if __name__ == "__main__":
    application = webapp.WSGIApplication(
                                     [('/login/google', LoginGoogle)],
                                     debug=True)
    run_wsgi_app(application)
