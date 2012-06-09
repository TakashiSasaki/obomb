from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm.session import sessionmaker
from unittest import TestCase, main
from logging import debug

class User(object):
    def __init__(self, name, fullname, password):
        """SQLAlchemy does not require this method"""
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        """SQLAlchemy does not require this method"""
        return "<User('%s','%s','%s')>" % (self.name, self.fullname, self.password)

class _Test(TestCase):
    def setUp(self):
        metadata = MetaData()
        self.usersTable = Table('users', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String),
                            Column('fullname', String),
                            Column('password', String))
        self.engine = create_engine("sqlite:///test2.sqlite", echo=True)
        metadata.create_all(self.engine)
        debug("metadata.create_all finished")
        from sqlalchemy.orm import mapper
        mapper(User, self.usersTable)

    def testAddRecord(self):
        ed_user = User('ed', "Ed Jones", "edpassword")
        debug (ed_user.fullname)
        debug (ed_user.password)
        
        Session = sessionmaker(bind=self.engine)
        session = Session()
        session.add(ed_user)
        session.commit()

if __name__ == "__main__":
    main()
