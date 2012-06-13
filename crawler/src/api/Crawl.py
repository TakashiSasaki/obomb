from __future__ import unicode_literals, print_function
__all__ = ["CrawlApp"]
from common import *
from webapp2 import RequestHandler, WSGIApplication
from paste.request import path_info_pop
from lib.Crawl import Crawl
from sqlalchemy.exc import *
from api.TableMixin import *

class _CrawlHandler(RequestHandler, TableMixin):
    table = Crawl
    def get(self):
        TableMixin.get(self)
        self.lastPathInfo = self.request.path_info

    def getLastPathInfo(self):
        return self.lastPathIngo

class CrawlApp(WSGIApplication):
    def __init__(self):
        WSGIApplication.__init__(self, [("/api/Crawl/?.*", _CrawlHandler)])
        
    def __call__(self, environ, start_response):
        path_info_pop(environ)
        path_info_pop(environ)
        #info("PATH_INFO = " + environ["PATH_INFO"]) 
        return WSGIApplication.__call__(self, environ, start_response)

class _(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        from random import randint
        self.port = randint(10000, 20000)
        from lib.WsgiRunner import PasteThread
        self.pasteThread = PasteThread(CrawlApp(), self.port, timeout=2)
        self.pasteThread.start()
        import time
        time.sleep(1)
        
    def testGet(self):
        self.assertTrue(self.pasteThread.isAlive())
        from httplib import HTTPConnection
        http_connection = HTTPConnection("localhost", port=self.port)
        http_connection.request("GET", "/api/Crawl")
        response = http_connection.getresponse()
        self.assertTrue(response.status == 404 or response.status == 200 or response.status == 500)
    
    def testGvizDataTable(self):
        session = SqlAlchemySessionFactory().createSqlAlchemySession()
        import gviz_api
        data_table = Crawl.getGvizDataTable()
        self.assertIsInstance(data_table, gviz_api.DataTable)
        import re
        r = re.compile(r"^google\.visualization\.Query\.setResponse\({.*}\);$")
        m = r.match(data_table.ToResponse())
        self.assertIsNotNone(m)
        session.close()
    
    def tearDown(self):
        TestCase.tearDown(self)
