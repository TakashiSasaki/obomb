from google.appengine.ext import db
from libobomb.VersionedItem import VersionedItemPolyModel
from libobomb.Iri import IriModel
from libobomb.ContentModel import ContentModel

#from multiprocessing.managers import SyncManager
#from google.appengine.api import users

class ExclusionModel(VersionedItemPolyModel):
    #exclusionId = db.IntegerProperty()
    exclusives = db.ListProperty(db.Key) # db.Key refers an instance of EquivalenceModel 
    #parentKnot = db.IntegerProperty()   
    #metadataIris = db.ListProperty(db.Key)
    #verse = db.Reference(VerseModel)
    #idnumber = db.IntegerProperty()
    #identityUri = db.ReferenceProperty(IriModel)
    #controlledBy = db.UserProperty()
    #createdDateTime = db.DateTimeProperty()
    #modifiedDateTime = db.DateTimeProperty()


import unittest
class Test(unittest.TestCase):
    def setUp(self):
        iri_model = IriModel()
        iri_model.originalUrl="http://example.com/test"
        iri_model.hierPart = [""]
        iri_model.query = ""
        iri_model.fragment = ""
        iri_model.put()

    def tearDown(self):
        pass

    def test_dummy(self):
        return True
        pass


