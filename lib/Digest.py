import io
import hashlib
import base64
import operator


class ReadBufferDigest(object):
    __slots__ = [ "sha1", "sha256", "md5", "histogram", "givenStartOffset", "givenEndOffset", "startOffset", "endOffset", "bufferedReader"]
    
    def __init__(self, buffered_reader, given_start_offset=0, given_end_offset= -1):
        assert isinstance(buffered_reader, io.BufferedReader)
        self.sha1 = hashlib.sha1()
        self.sha256 = hashlib.sha256()
        self.md5 = hashlib.md5()
        self.bufferedReader = buffered_reader
        self.histogram = [0] * 256
        self.givenStartOffset = given_start_offset
        self.givenEndOffset = given_end_offset
        self.startOffset = 0
        self.endOffset = -1
        self.done = False
    
    def SkipToGivenStartOffset(self):
        remaining_to_skip = self.givenStartOffset
        while remaining_to_skip > 0:
            dummy = self.bufferedReader.read(remaining_to_skip)
            remaining_to_skip -= len(dummy)
            self.startOffset += len(dummy)
    
    def ReadToGivenEndOffset(self):
        current_position = self.startOffset
        while True:
            if self.givenEndOffset == -1:
                r = self.bufferedReader.read()
            elif current_position <= self.givenEndOffset:
                r = self.bufferedReader.read(self.givenEndOffset - current_position + 1)
            else:
                break
                #raise RuntimeError("current_position=" + str(current_position) + " givenEndOffset=" + str(self.givenEndOffset))
            if len(r) == 0: break
            current_position += len(r)
            self.endOffset = current_position - 1
            self.sha256.update(r)
            self.sha1.update(r)
            self.md5.update(r)
            for b in r:
                self.histogram[ord(b)] += 1
        assert reduce(operator.add, self.histogram) == (current_position - self.startOffset)
    
    def StartOffset(self):
        assert self.endOffset >= 0
        return self.startOffset
    
    def EndOffset(self):
        assert self.endOffset >= 0
        return self.endOffset
    
    def TotalLength(self):
        assert self.endOffset >= 0
        if (self.givenEndOffset == -1) and (self.endOffset >= 0) :
            return self.endOffset
        else:
            raise RuntimeError("Total length is unknown.")
        
    def UrlSuffix(self):
        assert self.endOffset >= 0
        suffix = "/" + str(self.startOffset) + "-" + str(self.endOffset)
        if self.givenEndOffset == -1:
            suffix += "/" + str(self.endOffset + 1)
        return suffix

    def Md5Hex(self):
        assert self.endOffset >= 0
        return self.md5.hexdigest()
    
    def Md5Bytes(self):
        assert self.endOffset >= 0
        return self.md5.digest()

    def Md5Base32(self):
        assert self.endOffset >= 0
        return base64.b32encode(self.Md5Bytes())
    
    def Md5Uri(self, suffix=True):
        assert self.endOffset >= 0
        return "URN:MD5:" + self.Md5Base32() + self.UrlSuffix() if suffix else None

    def Sha1Hex(self):
        assert self.endOffset >= 0
        return self.sha1.hexdigest()
    
    def Sha1Bytes(self):
        assert self.endOffset >= 0
        return self.sha1.digest()
    
    def Sha1Base32(self):
        assert self.endOffset >= 0
        return base64.b32encode(self.Sha1Bytes())
    
    def Sha1Uri(self, suffix=True):
        """recommended because no padding"""
        assert self.endOffset >= 0
        return "URN:SHA1:" + self.Sha1Base32() + self.UrlSuffix() if suffix else None
    
    def Sha256Hex(self):
        assert self.endOffset >= 0
        return self.sha256.hexdigest()
    
    def Sha256Bytes(self):
        assert self.endOffset >= 0
        return self.sha256.digest()
    
    def Sha256Base32(self):
        assert self.endOffset >= 0
        return base64.b32encode(self.Sha256Bytes())
    
    def Sha256Uri(self, suffix=True):
        assert self.endOffset >= 0
        return "URN:SHA256:" + self.Sha256Base32() + self.UrlSuffix() if suffix else None
    
class FileDigest(ReadBufferDigest):
    def __init__(self, file_name, given_start_offset=0, given_end_offset= -1):
        buffered_reader = io.open(file_name, "rb")
        ReadBufferDigest.__init__(self, buffered_reader, given_start_offset, given_end_offset)
        self.SkipToGivenStartOffset()
        self.ReadToGivenEndOffset()

import unittest
class Test(unittest.TestCase):
    def setUp(self):
        self.digest1 = FileDigest("Digest.py")
        self.digest2 = FileDigest("Digest.py", 1)
        self.digest3 = FileDigest("Digest.py", 1, 1)
    
    def testFileIO(self):
        a = io.FileIO("Digest.py")
        assert isinstance(a, io.FileIO)
        a = io.open("Digest.py")
        assert isinstance(a, io.TextIOWrapper)
        a = io.open("Digest.py", "rb")
        assert isinstance(a, io.BufferedReader)
        a = open("Digest.py")
        assert isinstance(a, file)

    def testDigest(self):
        assert self.digest1.TotalLength() > 0
        assert len(self.digest1.Sha256Hex()) == 64
        assert len(self.digest1.Sha256Base32()) == 56
        print self.digest1.Sha256Uri()
        print self.digest1.Sha1Uri()
        print self.digest1.Md5Uri()
    
    def testStartOffset(self):
        assert self.digest2.TotalLength() > 0
        self.assertEqual(len(self.digest2.Sha1Base32()), 32)
        print self.digest2.Sha1Uri(True)
    
    def testEndOffset(self):
        self.assertRaises(RuntimeError, self.digest3.TotalLength)
        print self.digest3.Sha1Uri(True)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
