from libobomb.VersionedItem import VersionedItemPolyModel
from google.appengine.ext.db import ReferenceProperty, StringProperty,\
    ByteStringProperty, TextProperty, BlobProperty
from libobomb.Iri import IriModel
from google.appengine.ext.blobstore.blobstore import BlobReferenceProperty

class ContentModel(VersionedItemPolyModel):
    """Properties in this model never relies on other information
    except the data that sourceUri points to.
    SHA512 is the best on 64bit machine for now.
    """
    sourceUri = ReferenceProperty(IriModel)
    #sha512 = db.ByteStringProperty()
    contentString = StringProperty() #up to 500 characters
    contentByteString = ByteStringProperty() #Like StringProperty, except the value is not encoded in any way. The bytes are stored literally.
    contentText = TextProperty() #can store more than 500 characters. not indexed and cannot be used in filters or sort orders.
    
    #Binary data, as a byte string. This is a subclass of the built-in str type.
    #Blob properties are not indexed, and cannot be used in filters or sort orders.
    #Blob is for binary data, such as images. It takes a str value, 
    #but this value is stored as a byte string and is not encoded as text. 
    #Use a Text instance for large text data.
    contentBlob = BlobProperty()

    contentBlobReference = BlobReferenceProperty()
