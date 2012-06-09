from config import *
from sqlalchemy import  Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy import  MetaData as _MetaData
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
from sqlalchemy import Column
DeclarativeBase = _declarative_base(metadata=_MetaData())

class XYZ(DeclarativeBase):
    debug("XYZ start")
    __tablename__ = "XYZ"
    __table_args__ = {'sqlite_autoincrement': True}

    c1 = Column(Integer, primary_key = True)
    c2 = Column(String())
    c3 = Column(DateTime)
    c4 = Column(Boolean)

    debug("dropTable")
    @classmethod
    def dropTable(cls):
        try:
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            table.drop(engine, checkfirst=True)
        except:
            pass
    
    debug("createTable")
    @classmethod
    def createTable(cls):
        try:
            debug("try")
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            table.create(engine, checkfirst=True)
        except:
            pass
    debug("aend")

debug("_Test start")
class _Test(TestCase):
    
    def setUp(self):
        debug("setup start")
        #TestCase.setUp(self)
        XYZ.dropTable()
        #DeclarativeBase.metadata.create_all(engine)
        debug("setup end")

        
    def tearDown(self):
        debug("teardown start")
        #TestCase.tearDown(self)
        XYZ.dropTable()
        debug("teardown end")
        
    def test1(self):
        debug("test start")
        xyz = XYZ()
        debug(XYZ.__dict__)
        pass
        debug("test end")

if __name__ == "__main__":
    debug("main")
    main()