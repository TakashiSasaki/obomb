import uuid, base64, logging,re

_b64re = re.compile("([0-9A-Za-z+]+)==$")
_b32re = re.compile("([0-9A-Z]+)======$")

def GetBase32UuidWithPadding():
    u = uuid.uuid1()
    b32 = base64.b32encode(u.bytes)
    logging.log(logging.INFO, "generated uuid in base32 :" + b32)
    return b32

def GetBase64UuidWithPadding():
    u = uuid.uuid1()
    b64 = base64.b64encode(u.bytes)
    logging.log(logging.INFO, "generated uuid in base32 :" + b64)
    return b64

def GetBase32Uuid():
    b32match = _b32re.match(GetBase32UuidWithPadding())
    return b32match.group(1)

def GetBase64Uuid():
    b64match = _b64re.match(GetBase64UuidWithPadding())
    return b64match.group(1)

def DecodeBase32Uuid(b32string):
    return base64.b32decode(b32string+"======")

def DecodeBase64Uuid(b64string):
    return base64.b64decode(b64string+"==")

import unittest
class Test(unittest.TestCase):
    def setUp(self):
        l = logging.getLogger()
        l.setLevel(logging.DEBUG)
        pass
    def tearDown(self):
        pass

    def testBase32(self):
        b32 = GetBase32UuidWithPadding()
        assert _b32re.match(b32) is not None
        assert 16 == len(base64.b32decode(b32))
        b64 = GetBase64UuidWithPadding()
        assert _b64re.match(b64) is not None
        assert 16 == len(base64.b64decode(b64))
        assert 26 == len(GetBase32Uuid())
        assert 16 == len(DecodeBase32Uuid(GetBase32Uuid()))
        assert 22 == len(GetBase64Uuid())
        assert 16 == len(DecodeBase64Uuid(GetBase64Uuid()))
        logging.info(GetBase32Uuid())
        return True
    
