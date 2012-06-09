'''
Created on 2012/01/03

@author: Takashi
'''
from google.appengine.ext import db
import ObombUserKind
class SessionKind(db.Model):
    sessionId = db.StringProperty()
    obombUserEntity = db.ReferenceProperty(ObombUserKind.ObombUserKind)

SESSION_ID_KEY = "obomb_web_session_key"
