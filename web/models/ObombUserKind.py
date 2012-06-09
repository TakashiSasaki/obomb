'''
Created on 2012/01/03

@author: Takashi
'''
from google.appengine.ext import db
from TwitterUserKind import TwitterUserKind

class ObombUserKind(db.Model):
    """Obomb user is identified by email and can be bound with accounts on other services."""
    #__slot__ = ["googleUserIdentifier", "mixiUserIdentifier", "twitterUserIdentifier", "YahooJapanUserIdentifier"]
    googleUserIdentifier = db.StringProperty()
    twitterUserEntity = db.ReferenceProperty(TwitterUserKind)
    yahooJapanIdentifier = db.StringProperty()
    mixiUserIdentifier = db.StringProperty()
