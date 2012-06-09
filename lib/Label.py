from libobomb.VersionedItem import VersionedItemPolyModel
from google.appengine.ext.db import ListProperty, ReferenceProperty
from google.appengine.api.datastore import Key
from libobomb.ContentModel import ContentModel

class EquivalenceModel(VersionedItemPolyModel):
    """Pivot is a set of verses.
    It represents an abstraction or concept.
    pivotId is primary idNumber that is one of verses list. 
    """
    #equivalenceId = db.IntegerProperty()
    equivalents = ListProperty(Key) #db.Key refers an instance of ContentModel
    primaryVariant = ReferenceProperty(ContentModel, collection_name="primaryvariant_set")
    alphabeticVariant = ReferenceProperty(ContentModel, collection_name="alphabeticvariant_set")
    rubyVariant = ReferenceProperty(ContentModel, collection_name="rubyvariant_set")

class ExclusionModel(VersionedItemPolyModel):
    #exclusionId = db.IntegerProperty()
    exclusives = ListProperty(Key) # db.Key refers an instance of EquivalenceModel 
    #parentKnot = db.IntegerProperty()   
    #metadataIris = db.ListProperty(db.Key)
    #verse = db.Reference(VerseModel)
    #idnumber = db.IntegerProperty()
    #identityUri = db.ReferenceProperty(IriModel)
    #controlledBy = db.UserProperty()
    #createdDateTime = db.DateTimeProperty()
    #modifiedDateTime = db.DateTimeProperty()

