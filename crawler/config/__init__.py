from __future__ import  print_function, unicode_literals
import inspect as _inspect

def _getNameInPreviousFrame():
    current_frame = _inspect.currentframe(2)
    name = current_frame.f_globals["__name__"]
    return name

import logging as _logging
LOG_LEVEL = _logging.INFO
_logging.basicConfig(level=LOG_LEVEL)
logger = _logging.getLogger("")
logger.setLevel(LOG_LEVEL)

def debug(message):
    _logger = _logging.getLogger(_getNameInPreviousFrame())
    _logger.debug(message)

def info(message):
    _logger = _logging.getLogger(_getNameInPreviousFrame())
    _logger.info(message)

def warn(message):
    _logger = _logging.getLogger(_getNameInPreviousFrame())
    _logger.warn(message)

def error(message):
    _logger = _logging.getLogger(_getNameInPreviousFrame())
    _logger.error(message)

def critical(message):
    _logger = _logging.getLogger(_getNameInPreviousFrame())
    _logger.critical(message)

def exception(message):
    _logger = _logging.getLogger(_getNameInPreviousFrame())
    _logger.exception(message)

_userDirectory = None
def getUserDirectory():
    if _userDirectory is not None:
        return _userDirectory
    import os.path
    home_directory = os.path.expanduser("~")
    user_directory = os.path.join(home_directory, "obomb")
    if not os.path.exists(user_directory):
        import os
        os.mkdir(user_directory)
        if not os.path.exists(user_directory):
            raise IOError("User directory '" + user_directory + "' cannot be created.")
    return user_directory

def _getSqliteUrl():
    import os.path
    sqlite_path = os.path.join(getUserDirectory(), "obomb.db")
    info(sqlite_path) 
    sqlite_path_slash = sqlite_path.replace(os.path.sep, '/')
    info(sqlite_path_slash)
    sqlite_url = "sqlite:///" + sqlite_path_slash
    info(sqlite_url)
    return sqlite_url
    
#from logging import debug, info, warn, error, critical, exception
from unittest import TestCase, main
from sqlalchemy import create_engine as _create_engine
engine = _create_engine(_getSqliteUrl(), echo=False)
from sqlalchemy.orm.session import sessionmaker as _sessionmaker
Session = _sessionmaker(bind=engine, autocommit=False)
PersistentSession = _sessionmaker(bind=engine, autocommit=True)
#_metadata = MetaData()
from datetime import datetime as _datetime
from dateutil.tz import tzutc
def utcnow():
    dt = _datetime.utcnow();
    assert isinstance(dt, _datetime)
    assert dt.tzinfo is None
    dt2 = dt.replace(tzinfo=tzutc())
    return dt2

class _TestConfig(TestCase):
    def setUp(self):
        pass
    
    def testUtcnow(self):
        u = utcnow()
        self.assertIsInstance(u, _datetime, "utcnow() should returns an instance of datetime")
        self.assertIsNotNone(u.tzinfo, "utcnow() should returns aware datetime instance")
        info(u.ctime())
        l = _datetime.now()
        self.assertIsInstance(l, _datetime, "now() should returns an instance off datetime")
        self.assertIsNone(l.tzinfo, "now() should returns native datetime instance")
        info(l.ctime())
    
    def testDatabase(self):
        session = Session()
        session.close()
    
    def testStackTrace(self):
        info("testStackTrace")

if __name__ == "__main__":
    main()

