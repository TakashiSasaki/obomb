from __future__ import unicode_literals, print_function
__all__=["FileRecord"]

from common import *
from lib.Record import *
from lib.Crawl import *
from datetime import datetime, timedelta
from sqlalchemy.exc import *
from sqlalchemy import desc
import json

class FileRecord(Record):
    __slots__ = ("created")
    
    def __repr__(self):
        return self.toJson()
    
    def toJson(self):
        return json.dumps(self.__dict__)
    
    def exists(self, agent_id, session, best_before_period_in_second):
        last_file_info = getLastFileRecord(agent_id, self.url, session)
        if last_file_info is None: return False
        assert isinstance(last_file_info, Record)
        if last_file_info.lastSeen + timedelta(seconds=best_before_period_in_second) >= datetime.now():
            return True
        else:
            return False

    def setCreated(self, created_datetime):
        assert isinstance(created_datetime, datetime)
        assert created_datetime.tzinfo is not None
        self.created = created_datetime
    
    def getCreated(self):
        return self.created


def getLastFileRecord(agent_id, url, session):
    #print ("selecting for agentId = %d and url = %s" % (agent_id, url))
    my_object_my_crawl = session.query(Record, Crawl).filter(Crawl.agentId == agent_id).filter_by(url=url).order_by(desc(Record.lastSeen)).first()
    if my_object_my_crawl is None: return None
    assert isinstance(my_object_my_crawl[0], Record)
    assert isinstance(my_object_my_crawl[1], Crawl)
    return my_object_my_crawl[0]

class _(TestCase):
    def setUp(self):
        try:
            Crawl.dropTable()
        except OperationalError, e:
            debug(e.message)
        Record.dropTable()
        Crawl.createTable()
        Record.createTable()
        #self.session = Session()
    
    def testInsertOneRecord(self):
        session = SqlAlchemySessionFactory("obomb").createSqlAlchemySession()
        crawl = Crawl()
        crawl.begin()
        session.add(crawl)
        try:
            session.commit()
        except IntegrityError, e:
            session.close()
            Crawl.dropAndCreate(e.message)
            self.fail(e.message)
        file_info = FileRecord()
        file_info.setCrawlId(crawl.crawlId)
        file_info.setUrl("file:///c:/example")
        file_info.setLastSeen(utcnow())
        session.add(file_info)
        session.commit()
        file_info_2 = getLastFileRecord(crawl.agentId, "file:///c:/example", session)
        debug (file_info_2.crawlId)
        self.assertEqual(file_info_2.crawlId, crawl.crawlId)
        session.close()
        
