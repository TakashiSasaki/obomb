from google.appengine.ext.db import Model, URLProperty, StringListProperty, \
    StringProperty
    
class IriModel(Model):
    """
      URI         = scheme ":" hier-part [ "?" query ] [ "#" fragment ]
      hier-part   = "//" authority path-abempty / path-absolute / path-rootless / path-empty

       foo://example.com:8042/over/there?name=ferret#nose
       \_/   \______________/\_________/ \_________/ \__/
     scheme     authority       path        query   fragment
        |   _____________________|__
       / \ /                        \
       urn:example:animal:ferret:nose
    """
    originalUrl = URLProperty()
    hierPart = StringListProperty()
    query = StringProperty()
    fragment = StringProperty()
    
    def SetIri(self):
        """sets uri and its components.
        Each decomposed part will be normalized and decoded.
        Punycode and percent encoded string will be decoded.
        """
         
    def GetHierPart(self):
        """returns list of components in hier-part defined in RFC 3986.
        List includes sub-delim and colon.
        """
        return self.hierPart
        
    def GetQueryPart(self):
        return self.query

    def GetFragment(self):
        return self.fragment

###############################################################################
##################### THE FOLLOWING MODELS ARE OBSOLETED. #####################
###############################################################################

#class MetadataSuiteModel(db.Expando):
#    idnumber = db.IntegerProperty()
#    descriptiveMetadata = db.ReferenceProperty(DescriptiveMetadataModel)
#    technicalMetadata = db.ReferenceProperty(TechnicalMetadataModel)
#    administrativeMetadata = db.ReferenceProperty(AdministrativeMetadataModel)
#    structuralMetadata = db.ReferenceProperty(StructuralMetadataModel)
#    knot = db.ReferenceProperty(TagNodeModel)
#    obsoletedBy = db.SelfReference(collection_name="obsoletedBy_set")
#    equivalentTo = db.SelfReference(collection_name="equivalentTo_set")

#    def GetScheme(self):
#        """returns normalized scheme"""
#        scheme = self.scheme
#        r = re.compile("^[a-z0-9+-.]+$")
#        m = r.match(scheme)
#        assert m is not None
#        return scheme
    
#    def GetNonAuthority(self):
#        """returns list of non-authority components defined in RFC3986.
#        List includes sub-delim and colon.
#        """
#        return self.nonAuthority
    
#    def GetHost(self):
#        """returns normlized host if the url has authority part.
#        If original url does not have authority part, it returns None.
#        Since "file:///a.txt" does have zero-length authority part, it returns zero-length string.
#        """
#        host = self.host
#        if self.host is None: return None
#        r = re.compile("^[a-z0-9\.]*$")
#        m = r.match(host)
#        assert m is not None
#        return host
#    
#    def GetPort(self):
#        """returns port by int if the url has authority part with explicit port part.
#        port part could be lost while scheme based url normalization described in RFC3986.
#        """
#        port = self.port
#        assert port is None or isinstance(port, IntType)
#        return port
#    
#    def GetSegments(self):
#        """returns list of segments if the url has hier_part defined in RFC3986.
#        Leading slash of each segment is omitted.
#        Thus zero-length string represents slash itself.
#        """
#        return self.segments

#########################################################################################
########################## THE END OF OBSOLETED MODELS ##################################
#########################################################################################
