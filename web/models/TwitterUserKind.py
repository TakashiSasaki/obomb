'''
Created on 2012/01/03

@author: Takashi
'''
from google.appengine.ext import db
class TwitterUserKind(db.Model):
    """Twitter user is identified by integerId."""
    #__slot__ = ["googleUserIdentifier", "mixiUserIdentifier", "twitterUserIdentifier", "YahooJapanUserIdentifier"]
    integerId = db.IntegerProperty()
    screenName = db.StringProperty()
    accessToken = db.StringProperty()