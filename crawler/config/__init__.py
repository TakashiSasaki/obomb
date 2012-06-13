from __future__ import  print_function, unicode_literals

#from logging import debug, info, warn, error, critical, exception
#_metadata = MetaData()

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

