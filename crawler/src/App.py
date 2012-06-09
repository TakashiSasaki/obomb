from config import *
from webapp2 import RequestHandler, WSGIApplication
#from wsgiref.simple_server import demo_app


class _EnvironmentApp(WSGIApplication):
    class _EnvironmentHandler(RequestHandler):
        def get(self):
            import os
            self.response.out.write(os.environ)

    def __init__(self):
        WSGIApplication.__init__(self, [("/Environment", _EnvironmentApp._EnvironmentHandler),
                                        ("/environment", _EnvironmentApp._EnvironmentHandler)],
                                 debug=False, config=None)
        
from api.Record import RecordApp
from api.Crawl import CrawlApp

if __name__ == "__main__":
    from paste.urlparser import StaticURLParser
    html_app = StaticURLParser("html")
    css_app = StaticURLParser("css")
    js_app = StaticURLParser("js")
    
    from paste.cascade import Cascade
    cascaded_app = Cascade([html_app, css_app, js_app, _EnvironmentApp(), RecordApp(), CrawlApp()])
    while True:
        from lib.WsgiRunner import PasteThread
        paste_thread = PasteThread(cascaded_app, 10523, timeout=20)
        debug("starting PasteThread")
        paste_thread.start()
        debug("waiting for PasteThread to stop")
        try:
            paste_thread.join()
        except KeyError, e:
            pass
        info("restarting PasteThread")
        
    import webbrowser
    webbrowser.open("http://localhost:10523/Record.html", autoraise=1)

class _TestApp(TestCase):
    
    def setUp(self):
        TestCase.setUp(self)
        from random import randint
        self.port = randint(10000,20000)
        from lib.WsgiRunner import PasteThread
        self.pasteThread = PasteThread(CrawlApp(), self.port, timeout=5)
        self.assertIsNotNone(self.pasteThread.server)
        self.assertFalse(self.pasteThread.isAlive())
        self.assertTrue(self.pasteThread.server.running)
        self.pasteThread.start()
        self.assertTrue(self.pasteThread.isAlive())
        self.assertTrue(self.pasteThread.server.running)
        import time
        time.sleep(1)
        
    def testApiCrawl(self):
        from httplib import HTTPConnection
        http_connection = HTTPConnection("localhost", port=self.port)
        http_connection.request('GET', "/api/Crawl")
        response = http_connection.getresponse()
        info("reading body,m %d " % response.status)
        body = response.read()
        info(body)
        self.assertTrue(response.status == 500 or response.status == 404 or response.status == 200)
        self.assertGreater(len(body), 1)
        info("closing http connection")
        http_connection.close()
    
    def tearDown(self):
        info("shutting down PasteThread")
        self.pasteThread.shutdown()
        info("joining")
        self.pasteThread.join()
        TestCase.tearDown(self)
