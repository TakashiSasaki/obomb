'''
Created on 2012/01/21

@author: sasaki
'''
from google.appengine.ext.db.polymodel import PolyModel
from google.appengine.ext.db import StringProperty, EmailProperty,\
    DateTimeProperty, BooleanProperty, ListProperty, Model
from google.appengine.api.datastore_types import Key
from unittest.case import TestCase
from GaeAdopter import Initialize
from datetime import datetime

class BoundAccountModel(PolyModel):
    serviceName = StringProperty(required=True)
    loginName = StringProperty(required=True)

class ObombUserModel(Model):
    displayName = StringProperty(required=True)
    email = EmailProperty(required=True)
    email2 = EmailProperty()
    lastAccessTime = DateTimeProperty(required=True)
    deleted = BooleanProperty(required=True)
    boundAccounts = ListProperty(Key)

class Test(TestCase):
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    def testObombUserModel(self):
        Initialize("obomb")
        gql = ObombUserModel.gql("WHERE displayName = :1", ["TestUser"])
        for x in gql.fetch(1000):
            x.delete()
        self.assertEqual(0, gql.count())
        bound_account = BoundAccountModel(loginName="null", serviceName="Twitter")
        bound_account.put()
        obomb_user = ObombUserModel(displayName="TestUser", email="testuser@example.com", lastAccessTime=datetime.now(), deleted=False)
        obomb_user.boundAccounts = [bound_account.key()]
        obomb_user.put()     
        self.assertEqual(1, gql.count())
        instance = gql.get()
        instance.delete()
        self.assertEqual(0, gql.count())
