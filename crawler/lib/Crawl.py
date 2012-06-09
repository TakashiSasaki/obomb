from config import *
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime, timedelta
from lib.DeclarativeBase import DeclarativeBase
from lib.GvizDataTableMixin import GvizDataTableMixin
from lib.TableMixin import TableMixin
from sqlalchemy.exc import IntegrityError

class Crawl(DeclarativeBase, GvizDataTableMixin, TableMixin):
    __tablename__ = "Crawl"
    __table_args__ = {'sqlite_autoincrement': True}
    
    
    crawlId = Column(Integer(), primary_key=True, index=True, nullable=False)
    agentId = Column(String(), nullable=False, index=True) #MAC address can be used
    beginDateTime = Column(DateTime(), nullable=False, index=True)
    endDateTime = Column(DateTime(), nullable=True, index=True)
    userName = Column(String(), nullable=False, index=True)
    userDomain = Column(String(), nullable=False, index=True)
    nProcessedItems = Column(Integer(), nullable=True, index=False)
    nProcessedBytes = Column(Integer(), nullable=True, index=False)
    completed = Column(Boolean(), nullable=False, index=False, default=False)
    archived = Column(Boolean(), nullable=False, index=True, default=False)
    starred = Column(Boolean(), nullable=False, index=True, default=False)
    uploaded = Column(Boolean(), nullable=True, index=True, default=False)
    
    def __init__(self, email_style_user_identifier=None):
        from uuid import getnode
        self.agentId = getnode()
        if email_style_user_identifier is None:
            self._setUserByEnvironment()
        else:
            self._setUserByEmail(email_style_user_identifier)
        self.nProcessedBytes = 0
        self.nProcessedItems = 0
    
    def _setUserByEmail(self, email):
        import re
        p = re.compile("^([^@]+)@([^@]+)$")
        m = p.match(email)
        try:
            user_name = m.group(1)
            user_domain = m.group(2)
            assert user_name is not None
            assert user_domain is not None
            self.userName = user_name
            self.userDomain = user_domain
        except:
            self.userName = None
            self.userDomain = None
        
    def _setUserByEnvironment(self):
        import os
        try:
            user_name = os.environ.get("USERNAME")
            assert user_name is not None
        except:
            user_name = None
        self.userName = user_name
        try:
            import socket  
            host_name = socket.gethostname()
            assert host_name is not None  
        except:
            host_name = None
        self.userDomain = host_name
        
    def begin(self):
        self.beginDateTime = datetime.now()
    
    def end(self):
        self.endDateTime = datetime.now()

    def increment(self, processed_bytes):
        self.nProcessedBytes += processed_bytes
        self.nProcessedItems += 1
        
    def getNumberOfProcessedBytes(self):
        return self.nProcessedBytes
    
    def getNumberOfProcessedItems(self):
        return self.nProcessedItems
    
    def getElapsedSeconds(self):
        now = datetime.now()
        elapsed = now - self.beginDateTime
        assert isinstance(elapsed, timedelta)
        return elapsed.total_seconds()
    
    def getFilesPerSecond(self):
        return self.getNumberOfProcessedItems() / self.getElapsedSeconds()
    
    def getBytesPerSecond(self):
        return self.getNumberOfProcessedBytes() / self.getElapsedSeconds()
    
    @classmethod
    def dummy(cls, n_dummy = 1):
        session = Session()
        from uuid import uuid1
        n_before = cls.count()
        dummy_crawl = None
        for x in range(n_dummy):
            dummy_crawl = Crawl()
            assert isinstance(dummy_crawl, Crawl)
            dummy_crawl.begin()
            dummy_crawl.end()
            dummy_crawl.agentId = uuid1().get_hex()
            session.add(dummy_crawl)
        session.commit()
        n_after = cls.count()
        assert n_before + n_dummy == n_after
        info(dummy_crawl)
        assert isinstance(dummy_crawl, Crawl)
        return dummy_crawl
    
class _TestLibCrawl(TestCase):
    def setUp(self):
        #DeclarativeBase.metadata.create_all(engine)
        #if Crawl.exists():
        #    Crawl.dropTable()
        #self.assertFalse(Crawl.exists(), "Crawl table should be deleted at the start of tests.")
        Crawl.createTable()
        self.assertTrue(Crawl.exists(), "Crawl table does not exists.")
    
    def testDummy(self):
        dummy = Crawl.dummy()
        self.assertIsInstance(dummy, Crawl)

    def testAutoIncrement(self):
        session = Session()
        my_crawl_1 = Crawl()
        my_crawl_1.begin()
        my_crawl_1.end()
        session.add(my_crawl_1)
        my_crawl_2 = Crawl()
        my_crawl_2.begin()
        my_crawl_2.end()
        session.add(my_crawl_2)
        try:
            session.commit()
        except IntegrityError,e:
            session.close()
            Crawl._dropAndCreate(e.message)
            self.fail(e.message)
            
        self.assertEqual(my_crawl_1.crawlId + 1, my_crawl_2.crawlId)
        session.close()
    
    def testGvizSchema(self):
        info("testGvizSchema")
        debug(Crawl.getGvizSchema())
    
    def testGvizData(self):
        debug("testGvizData")
        crawl = Crawl()
        debug(crawl.getGvizData())

    def testGvizDataTable(self):
        debug("testGvizDataTable")
        session = Session()
        crawl = Crawl()
        crawl.begin()
        crawl.end()
        session.add(crawl)
        try:
            session.commit()
        except IntegrityError, e:
            session.close()
            Crawl.dropAndCreate(e.message)
            self.fail(e.message)
        session.close()
        session = Session()
        info(Crawl.getGvizDataTable(session).ToJSonResponse())
        session.close()

if __name__ == "__main__":
    main()
