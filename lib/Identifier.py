# -*- coding: utf-8 -*- 
'''
@author: Takashi SASAKI
@contact: http://twitter.com/TakashiSasaki

'''
from datetime import datetime 
from google.appengine.ext.db import URLProperty, StringListProperty, \
    ListProperty, BooleanProperty, ReferenceProperty, StringProperty, Model, \
    SelfReferenceProperty, DateTimeProperty, GeoPt, GqlQuery
from google.appengine.api.datastore import Key, DatastoreAdapter
from GaeAdopter import Initialize
from libobomb.Uuid import GetBase32Uuid
from google.appengine.ext.db.polymodel import PolyModel
from libobomb.VersionedItem import VersionedItemPolyModel
from unittest.case import TestCase
import urllib2
from urllib import pathname2url
from urlparse import urlparse
from furl.furl import furl
from google.appengine.api.datastore_errors import BadValueError
from google.appengine.api.apiproxy_stub_map import apiproxy
from google.appengine.api import datastore
from google.appengine.ext.db.stats import KindStat
from GaeAdopter.GaeAdopter import GaeAdopter
from google.appengine.ext.db.metadata import Kind
from logging import getLogger, debug, DEBUG

class WordsModel(PolyModel):
    words = StringListProperty()
    
class LabelsModel(WordsModel):
    pass
    
class CircumstanceModel(WordsModel):
    pass

class ContentModel(WordsModel):
    pass

def IsInstances(list_, class_):
    assert isinstance(list_, list) or isinstance(list_, tuple)
    assert isinstance(class_, type)
    for x in list_:
        if not isinstance(x, class_):
            return False
    return True

def TimeSpacePoint():
    pass
    
class IdentifierModel(VersionedItemPolyModel):
    identifierString = StringProperty(required=True)
    fileLocations = StringListProperty()
    fileLocationTimes  = ListProperty(datetime)
    geoLocations = ListProperty(GeoPt)
    geoLocationTimes = ListProperty(datetime)
    labels = StringListProperty()
    circumstances = ListProperty(Key)
    contents = ListProperty(Key)
    observedTimes = ListProperty(datetime)
    metadataList = ListProperty(Key)
    #children = ListProperty(Key)
    #complete = BooleanProperty()
    includeIn = SelfReferenceProperty()
    def setCircumstances(self, circumstances_):
        pass

#class ContainmentModel(VersionedItemPolyModel):
#   parentIdentifier = ReferenceProperty(IdentifierModel)
#   childrenIdentifiers = ListProperty(Key)
#    completeness = BooleanProperty()

class Test(TestCase):
    getLogger().setLevel(DEBUG)
    Initialize("obomb")
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def testSomething(self):
        identifier = IdentifierModel(lockBegins=datetime.now(), lockEnds=datetime.now(), identifierString="urn:uuid:" + GetBase32Uuid(),
                                     owner=22222, versionNumber=1111, locationString="http://exmaple.com/a/b/c"
                                     , item=456, labels =["label1", "label2"])
        identifier.circumstancesKeywords = ["いちご", "メロン"]
        identifier.contentsKeywords = ["動物", "植物"]
        identifier.put()
        gql = IdentifierModel.gql("")
        try:    
            for x in gql.fetch(100):
                assert isinstance(x, IdentifierModel)
                print x
        except BadValueError, e:
            self.logger.error(str(e))
        
        q = GqlQuery("SELECT * FROM IdentifierModel")
        self.logger.debug("SELECT * FROM IdentifierModel results %s items"% len(q))

    def testClassType(self):
        class A(object):
            pass
        alist = [A(), A(), A()]
        assert IsInstances(alist, A)
        self.logger.info(type(A))
    
    def testTraverse(self):
        logger = getLogger().getChild("testTraverse")
        import os
        file_counter = 0
        dir_counter = 0
        for root, dirs, files in os.walk(".."):
            for file in files:
                file_counter += 1
                path = os.path.abspath(os.path.join(root, file))
                url = "file://localhost" + pathname2url(path)[2:]
                logger.debug("file[" + str(file_counter) + "]" + url)
                #identifier = IdentifierModel() 
            for dir in dirs:
                dir_counter += 1
                path = os.path.abspath(os.path.join(root, dir))
                url = "file://localhost" + pathname2url(path)[2:]
                logger.debug("dir[" + str(dir_counter) + "]" + url)
            f = furl("http://a.example.com/path/http://b.example.com/xyz.html")
            logger.debug(f.url)
    
    def testGetKinds(self):
        logger = getLogger().getChild(__name__)
        Initialize("obomb")
        q = Kind.all()
        for kind in q.fetch(100):
            logger.info(kind.kind_name)
    
if __name__ == "__main__":
    class A(object):
        pass
    print type(A)
    print isinstance(A, type)
    
