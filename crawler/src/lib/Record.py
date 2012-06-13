from __future__ import unicode_literals, print_function
from common import *
#from __future__ import unicode_literals, print_function
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relation, relationship
from sqlalchemy.exc import IntegrityError
from datetime import datetime
#from MyCrawlTable import MyCrawlTable
#from MyCrawl import MyCrawl
#from lib.Crawl import *
from lib.GvizDataTableMixin import GvizDataTableMixin
from lib.DeclarativeBase import DeclarativeBase
from lib.TableMixin import TableMixin

class Record(DeclarativeBase, GvizDataTableMixin, TableMixin):
    __tablename__ = "Record"
    __table_args__ = {'sqlite_autoincrement': True}
    engine = SqlAlchemyEngine().getEngine()
    
    objectId = Column(Integer, primary_key=True, index=True, nullable=False) #unique only on this database
    def getObjectId(self):
        """objectId is the primary key and automatically set"""
        return self.objectId
    
    crawlId = Column(Integer, ForeignKey('Crawl.crawlId'), index=True, nullable=False) #identical for one session
    #crawl = relationship("Crawl", backref="record")
    
    def getCrawlId(self):
        """crawlId is given for one crawl and is a foreign key of MyCrawl table."""
        return self.crawlId
    def setCrawlId(self, crawl_id):
        assert isinstance(crawl_id , int)
        self.crawlId = crawl_id
    
    uri = Column(String(), index=True, nullable=True)
    def getUri(self):
        return self.uri
    def setUri(self, uri_):
        assert isUnicode(uri_), "URI must be unicode string"
        from urlparse import urlsplit, urlunsplit
        split_uri = urlsplit(uri_, allow_fragments=True)
        assert isinstance(split_uri, tuple)
        unsplit_uri = urlunsplit(split_uri)
        if unsplit_uri != uri_:
            debug(unsplit_uri + " != " + uri_)
            raise Exception("%s != %s " % (unsplit_uri , uri_))
        self.uri = uri_

    url = Column(String(), index=True, nullable=True)
    def getUrl(self):
        return self.url
    def setUrl(self, url_):
        assert isUnicode(url_), "URL must be unicode string"
        from urlparse import urlparse, ParseResult
        parse_result = urlparse(url_, allow_fragments=True)
        rebuilt_url = parse_result.geturl()
        if rebuilt_url != url_:
            raise Exception("malformed URL: " + url_)
        if parse_result[0] not in ("http", "file", "https", "ftp", "file"):
            raise Exception("unacceptable scheme for URL: + " + parse_result["scheme"])
        self.url = url_
    
    size = Column(Integer(), nullable=True, index=True)
    def getSize(self):
        return self.getSize()
    def setSize(self, size_):
        assert isinstance(size_, long)
        self.size = size_

    lastModified = Column(DateTime(), index=True, nullable=True) #last modified datetime
    def getLastModified(self):
        return self.lastModified
    def setLastModified(self, last_modified):
        assert isinstance(last_modified, datetime)
        assert last_modified.tzinfo is not None # avoid naive datetime
        self.lastModified = last_modified
    
    lastSeen = Column(DateTime(), index=True, nullable=False) #last seen datetime
    def getLastSeen(self):
        return self.lastSeen
    def setLastSeen(self, last_seen):
        assert isinstance(last_seen, datetime)
        assert last_seen.tzinfo is not None
        self.lastSeen = last_seen

    jsonString = Column(String(), nullable=True) #serialized data
    def getJsonString(self):
        return self.jsonString
    def setJsonString(self, json_string):
        assert isUnicode(json_string), "JSON string must be unicode string"
        from json import loads, dumps
        x = loads(json_string)
        self.jsonString = dumps(x)
    
    belongsTo = Column(Integer(), index=True, nullable=True)
    def getBelongsTo(self):
        return self.belongsTo
    def setBelongsTo(self, belongs_to):
        assert isinstance(belongs_to, int)
        self.belongsTo = belongs_to 
        
    exhaustive = Column(Boolean(), nullable=False, index=True, default=False)
    def getExhaustive(self):
        return self.getCompleted()
    def setExhaustive(self, is_completed):
        assert isinstance(is_completed, bool)
        self.completed = is_completed
        
    archived = Column(Boolean(), index=True, nullable=False, default=False)
    starred = Column(Boolean(), index=True, nullable=False, default=False)
    uploaded = Column(Boolean(), index=True, nullable=False, default=False)
    
    memo0 = Column(String(), nullable=True)
    memo1 = Column(String(), nullable=True)
    memo2 = Column(String(), nullable=True)
    memo3 = Column(String(), nullable=True)
    memo4 = Column(String(), nullable=True)
    memo5 = Column(String(), nullable=True)
    memo6 = Column(String(), nullable=True)
    memo7 = Column(String(), nullable=True)
    memo8 = Column(String(), nullable=True)
    memo9 = Column(String(), nullable=True)

    def __str__(self):
        s = "<Record(%s,%s,%s,%s,%s)>" % (self.url, self.size, self.lastModified, self.lastSeen, self.uri)
        return s

    @classmethod
    def dropTable(cls):
        try:
            my_object_table = DeclarativeBase.metadata.tables[cls.__tablename__]
            my_object_table.drop(cls.engine, checkfirst=True)
        except Exception, e:
            info(e)
        
    @classmethod
    def createTable(cls):
        try:
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            table.create(cls.engine, checkfirst=True)
        except Exception, e:
            info(e)

    @classmethod
    def dropAndCreateTable(cls, message):
            print(message)
            x = raw_input("Drop and create Record table ? (Y/n) : ")
            if x == "Y":
                cls.dropTable()
                cls.createTable()

    @classmethod
    def insertDummyRecords(cls, n_dummy):
        n_before = cls.count()
        session = SqlAlchemySessionFactory().createSqlAlchemySession()
        record = None
        for x in range(n_dummy):
            #crawl = Crawl.dummy()
            record = Record()
            from random import randint
            record.crawlId = randint(10,99)
            record.size = randint(1000, 9999)
            from uuid import uuid1
            record.uri = "http://example.com/" + uuid1().get_hex()
            record.url = "http://exmaple.com/" + uuid1().get_hex()
            record.lastSeen = utcnow()
            record.lastModified = utcnow()
            record.jsonString = "{}"
            record.belongsTo = None
            record.exhaustive = False
            session.add(record)
        session.commit()
        n_after = cls.count()
        assert n_before + n_dummy == n_after
        assert isinstance(record, Record)
        return record
    

class MemoMap(DeclarativeBase):
    __tablename__ = "MemoMap"
    memoId = Column(Integer, primary_key=True)
    memoName = Column(String(), nullable=False)
    def __init__(self, memo_id, memo_name):
        self.memoId = memo_id
        self.memoName = memo_name

class _TableOperation(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        from lib.Crawl import Crawl
        if not Crawl.exists():
            Crawl.createTable()
        self.assertTrue(Crawl.exists())
        
    def tearDown(self):
        TestCase.tearDown(self)
        
    def testCreateAndDropTable(self):
        Record.dropTable()
        self.assertFalse(Record.exists())
        Record.createTable()
        self.assertTrue(Record.exists())
        Record.dropTable()
        self.assertFalse(Record.exists())

class _RecordOperation(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        from lib.Crawl import Crawl
        self.assertTrue(Crawl.exists())
        Record.createTable()
        self.assertTrue(Record.exists())
        
    def tearDown(self):
        Record.dropTable()
        self.assertFalse(Record.exists())
        TestCase.tearDown(self)
        
    def testInsertDummyRecords(self):
        Record.insertDummyRecords(10)
        self.assertEqual(Record.count(), 10)
