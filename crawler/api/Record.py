from config import *
from webapp2 import RequestHandler, WSGIApplication
from paste.request import path_info_pop
from lib.Record import Record
from sqlalchemy.exc import OperationalError

class _RecordHandler(RequestHandler):
    def get(self):
        self.response.out.write(self.request.path_info)
        if self.request.path_info == "":
            session = Session()
            try:
                data_table = Record.getGvizDataTable(session)
                session.close()
            except OperationalError, e:
                self.response.set_status(404)
                self.response.out.write(e.message)
                return
            self.response.out.write(data_table.ToJSonResponse())

class RecordApp(WSGIApplication):
    def __init__(self):
        WSGIApplication.__init__(self, [("/api/Record/?.*", _RecordHandler)])
        
    def __call__(self, environ, start_response):
        path_info_pop(environ)
        path_info_pop(environ)
        #info("PATH_INFO = " + environ["PATH_INFO"]) 
        return WSGIApplication.__call__(self, environ, start_response)

class _Test(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test(self):
        record_app = RecordApp()
    
    def tearDown(self):
        TestCase.tearDown(self)
        
if __name__ == "__main__":
    main()
