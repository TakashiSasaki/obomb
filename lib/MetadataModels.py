"""classes in this module are obsoleted."""

from google.appengine.api import users
from libobomb.VersionedItem import VersionedItemPolyModel
from libobomb.ContentModel import ContentModel
from google.appengine.ext.db import ReferenceProperty, ListProperty, Expando,\
    IntegerProperty, StringProperty, StringListProperty, DateTimeProperty,\
    URLProperty, GeoPtProperty, UserProperty
from google.appengine.api.datastore_types import Key

class PredicationModel(VersionedItemPolyModel):
    """A predication is a pair of two terms."""
    #predicationId = db.IntegerProperty()
    arc = ReferenceProperty(ContentModel, collection_name="arc_set")
    node = ReferenceProperty(ContentModel, collection_name="node_set")


class MetadataModel(VersionedItemPolyModel):
    """A metadata is a set of predications"""
    #metadataId = db.IntegerProperty()
    predications = ListProperty(Key) # db.Key refers an instance of PredicationModel


# just FYI, obsoleted
class DescriptiveMetadataModel(Expando):
    """Descriptive metadata describes resource for purposes such as discovery and identification. 
    It can include elements such as title, abstract, author, and keywords. (NISO, ISBN 1-880124-62-9)
    In obomb, this model is indented to hold most generic information.
    They are self descriptive, independent from environment and media.
    """
    idnumber = IntegerProperty()
    title = StringProperty()
    keywords = StringListProperty()
    authors = StringListProperty()


class TechnicalMetadataModel(Expando): 
    """Technical metadata focuses on how a digital object was created, its format, 
    format-specific technical characteristics, storage and location, etc. 
    Accurate technical metadata helps a repository manage digital 
    objects over time and keep them usable. 
    (http://hul.harvard.edu/ois/digproj/metadata-standards.html)
    """
    idnumber = IntegerProperty()
    messageDigest = StringProperty()
    size = IntegerProperty()
    owner = StringProperty()
    createdDateTime = DateTimeProperty()
    modifiedDateTime = DateTimeProperty()    
    url = URLProperty()
    geo = GeoPtProperty()

class AdministrativeMetadataModel(Expando):
    idnumber = IntegerProperty()
    controlledBy = UserProperty()
    lastSeenDateTime = DateTimeProperty()
    lastSeenBy = StringProperty()
    lastSeenFrom = StringProperty()
    incomingToken = StringProperty()
    outgoingToken = StringProperty()
    allowedUsers = ListProperty(users.User)

class StructuralMetadataModel(Expando):
    """Structural metadata indicates how compound objects are pot together,
    for example, how pages are ordered to form chapters. (NISO ISBN 1-880124-62-9)
    METS (Metadata Encoding & Transmission Standard) includes structural metadata standard.
    """
    idnumber = IntegerProperty()

def deprecated(f):
    def _(*args, **keywords):
        print args, keywords
        f(*args, **keywords)
    return _

@deprecated
class A(object):
    pass

if __name__ == "__main__":
    a = A()
    print 123