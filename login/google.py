'''
Created on 2012/01/03

@author: Takashi SASAKI
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class LoginGoogle(webapp.RequestHandler):
    def get(self):
        self.response.out.write("<html><body>")
        self.response.out.write("<p>currently not implemented</p>")
        self.response.out.write("</body></html>")
    
    def post(self):
        self.get()

if __name__ == "__main__":
    application = webapp.WSGIApplication(
                                     [('/login/google', LoginGoogle)],
                                     debug=True)
    run_wsgi_app(application)
