'''
Created on 2012/01/19

@author: Takashi
'''
from google.appengine.ext.db.polymodel import PolyModel
from google.appengine.ext.db import DateTimeProperty, IntegerProperty, ReferenceProperty
from unittest.case import TestCase
import datetime
from GaeAdopter import Initialize
from libobomb.User import ObombUserModel

class VersionedItemPolyModel(PolyModel):
    """This class models hub style data synchronizing system.
    idNumber is signed integer.    
    zero indicates invalid ID number.
    negative idNumber indicates local ID number.
    positive idNumber is assigned by obomb web service and globally unique.
    None owner indicates that the instance is well-known and authorized by standards outside.
    """
    item = IntegerProperty(required=True)
    owner = IntegerProperty(required=True)
    lockBegins = DateTimeProperty(required=True)
    lockEnds = DateTimeProperty(required=True)
    versionNumber = IntegerProperty(required=True)
    
    #lastUploaded = db.DateTimeProperty()
    #lastDownloaded = db.DateTimeProperty()
    #lastStableDurationBegins = db.DateTimeProperty()
    #lastStableDurationEnds = db.DateTimeProperty()

class Test(TestCase):
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    def startUp(self):
        pass
    
    def tearDown(self):
        pass

    def testVersionedItemPolyModel(self):
        Initialize("obomb")
        obomb_user = ObombUserModel(displayName="TestUser", email="testuser@example.com", lastAccessTime=datetime.datetime.now(), deleted=False)
        obomb_user_key = obomb_user.put()
        gql = VersionedItemPolyModel.gql("WHERE owner = :1", [obomb_user_key])
        self.logger.debug(obomb_user_key.__str__())
        for x in gql.fetch(100):
            x.delete()
        self.assertEqual(0, gql.count())
        versioned_item = VersionedItemPolyModel(owner=obomb_user_key, lockBegins=datetime.datetime.now(), lockEnds=datetime.datetime.now(), versionNumber=12345)
        versioned_item.put()
        self.assertEqual(1, gql.count())
        versioned_item.delete()
        self.assertEqual(0, gql.count())
