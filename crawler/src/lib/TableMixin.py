from config import *
from sqlalchemy import Table

class TableMixin(object):
    
    @classmethod
    def getTable(cls):
        assert isinstance(cls.__tablename__, str)
        table = cls.getMetadata().tables[cls.__tablename__]
        assert isinstance(table, Table)
        return table

    @classmethod
    def exists(cls):
        table = cls.getTable()
        return table.exists(engine)
    
    @classmethod
    def dropTable(cls):
        warn("table %s is being dropped" % cls.getTable())
        try:
            table = cls.getTable()
            debug("dropping table " + str(table))
            table.drop(engine, checkfirst=True)
        except Exception, e:
            exception(e.message)
            raise e
        
    @classmethod
    def createTable(cls):
        try:
            table = cls.getTable()
            table.create(engine, checkfirst=True)
        except Exception, e:
            exception(e.message)
            raise e
    
    @classmethod
    def dropAndCreate(cls, message):
            print(message)
            x = raw_input("Drop and create %s table ? (Y/n) : " % cls.getTable())
            if x == "Y":
                cls.dropTable()
                cls.createTable()
    
    @classmethod
    def count(cls):
        session = Session()
        query = session.query(cls)
        c = query.count()
        session.close()
        return c

    @classmethod
    def getQuery(cls):
        session = Session()
        query = session.query(cls.getTable())
        return query