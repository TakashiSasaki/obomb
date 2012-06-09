from config import *
from gviz_api import DataTable
from sqlalchemy import Column
from sqlalchemy.orm.query import Query
from sqlalchemy.types import BigInteger, Boolean, Date, DateTime, Enum, Float, Integer, Interval, LargeBinary, Numeric
from sqlalchemy.types import PickleType, SchemaType, SmallInteger, String, Text, Time, Unicode, UnicodeText
from sqlalchemy.types import BIGINT, BINARY, BLOB, BOOLEAN, CHAR, CLOB, DATE, DATETIME, DECIMAL, FLOAT, INTEGER
from sqlalchemy.types import INT, NCHAR, NVARCHAR, NUMERIC, REAL, SMALLINT, TEXT, TIME, TIMESTAMP, VARBINARY, VARCHAR
from inspect import isclass

GVIZ_STRING = "string"
GVIZ_NUMBER = "number"
GVIZ_BOOLEAN = "boolean"
GVIZ_DATE = "date"
GVIZ_DATETIME = "datetime"
GVIZ_TIMEOFDAY = "timeofday"

STRING_CLASSES = [String, Text, Unicode, UnicodeText, CHAR, NCHAR, NVARCHAR, TEXT, VARCHAR]
NUMBER_CLASSES = [BigInteger, Float, Integer, Numeric, SmallInteger, BIGINT, FLOAT, INTEGER, DECIMAL, SMALLINT, INT, NUMERIC, REAL,]
BOOLEAN_CLASSES = [Boolean, BOOLEAN]
DATE_CLASSES = [Date, DATE]
DATETIME_CLASSES = [DateTime, DATETIME]
TIMEOFDAY_CLASSES = [Time, TIME]

class GvizDataTableMixin(object):
    
    @classmethod
    def getMetadata(cls):
        return cls.metadata
    
    @classmethod
    def getColumns(cls):
        return cls.__table__.columns
    
    @classmethod
    def getGvizSchema(cls):
        gviz_schema = []
        for column in cls.getColumns():
            assert isinstance(column, Column)
            n = column.name
            assert isinstance(n, str)
            t = column.type
            if type(t) in STRING_CLASSES:
                gviz_schema.append((n, GVIZ_STRING))
            elif type(t) in NUMBER_CLASSES:
                gviz_schema.append((n, GVIZ_NUMBER))
            elif type(t) in BOOLEAN_CLASSES:
                gviz_schema.append((n, GVIZ_BOOLEAN))
            elif type(t) in DATE_CLASSES:
                gviz_schema.append((n, GVIZ_DATE))
            elif type(t) in DATETIME_CLASSES:
                gviz_schema.append((n, GVIZ_DATETIME))
            elif type(t) in TIMEOFDAY_CLASSES:
                gviz_schema.append((n, GVIZ_TIMEOFDAY))
            else:
                raise TypeError("column %s has unknown type %s" % (n, type(t)))
        return gviz_schema
    
    def getGvizData(self):
        gviz_data = []
        for column in self.getColumns():
            assert isinstance(column, Column)
            n = column.name
            assert isinstance(n, str)
            v = getattr(self, n)
            gviz_data.append(v)
        return gviz_data
    
    @classmethod
    def getGvizDataTable(cls, session):
        assert isclass(cls)
        query = session.query(cls)
        assert isinstance(query, Query)
        data_table = DataTable(cls.getGvizSchema())
        for x in query.all():
            gviz_data = x.getGvizData()
            assert isinstance(gviz_data, list)
            data_table.AppendData([gviz_data])
        return data_table

class _Test(TestCase):
    def setUp(self):
        TestCase.setUp(self)
    
    def tearDown(self):
        TestCase.tearDown(self)
