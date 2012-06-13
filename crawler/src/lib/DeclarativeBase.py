from __future__ import unicode_literals, print_function
__all__=["DeclarativeBase"]

from common import *
from sqlalchemy import  MetaData as _MetaData
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
#DeclarativeBase = _declarative_base(metadata=_MetaData())
DeclarativeBase = _declarative_base()
from sqlalchemy import  Column, String, Integer, DateTime, Boolean

class _XYZ(DeclarativeBase):
    debug("XYZ start")
    __tablename__ = "XYZ"
    __table_args__ = {'sqlite_autoincrement': True}

    c1 = Column(Integer, primary_key=True)
    c2 = Column(String())
    c3 = Column(DateTime)
    c4 = Column(Boolean)

    @classmethod
    def dropTable(cls):
        try:
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            engine = SqlAlchemyEngine().getEngine()
            table.drop(engine, checkfirst=True)
        except:
            pass
    
    @classmethod
    def createTable(cls):
        try:
            debug("try")
            table = DeclarativeBase.metadata.tables[cls.__tablename__]
            engine = SqlAlchemyEngine().getEngine()
            table.create(engine, checkfirst=True)
        except:
            pass

import unittest
class _(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        
    def testDeclarativeBase(self):
        debug("test start")
        xyz = _XYZ()
        _XYZ.dropTable()
