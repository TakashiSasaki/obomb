from config import *
from webapp2 import RequestHandler, WSGIApplication

class MyHandler(RequestHandler):
    def get(self):
        info("MyHandler.get was called")
        self.response.out.write("I'm a WSGI application built on webapp2 framework.")

class MyApp(WSGIApplication):
    def __init__(self):
        WSGIApplication.__init__(self, [("/", MyHandler)])

from paste.urlmap import URLMap
from paste.urlparser import StaticURLParser
from paste.fileapp import FileApp
from paste.evalexception.middleware import EvalException
import paste.translogger
def MyApp2():
    urlMap = URLMap()
    urlMap["/"] = MyApp()
    urlMap["/static"] = StaticURLParser("static")
    urlMap["/favicon.ico"] = FileApp("static/favicon.ico")
    evalException = EvalException(urlMap)
    f = ('[%(time)s] "%(REQUEST_METHOD)s '
              '%(REQUEST_URI)s %(HTTP_VERSION)s" '
              '%(status)s %(bytes)s')
    app = paste.translogger.make_filter(evalException, {}, format=f)
    return app
