# -*- coding:utf-8 -*-

import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

class RequestHandlerMod(webapp.RequestHandler):
    def __init__(self, *args):
        super(RequestHandlerMod, self).__init__(*args)
        
        if self.request.headers["Accept"].find("html") != -1:
            self.response.headers['Content-Type'] = 'text/html'
            self.response_type = "html"
        elif self.request.headers["Accept"].find("json") != -1:
            self.response.headers['Content-Type'] = 'application/json'
            self.response_type = "json"
        elif self.request.headers["Accept"].find("javascript") != -1:
            self.response.headers['Content-Type'] = 'application/javascript'
            self.response_type = "javascript"
        elif self.request.headers["Accept"].find("xml") != -1:
            self.response.headers['Content-Type'] = 'application/xml'
            self.response_type = "xml"
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response_type = "text"

class Post:
    class New(RequestHandlerMod):
        def get(self):
            template_values = {
                               "header": str(self.request.headers)
                               }
            path = os.path.join(os.path.dirname(__file__), 'templates/html/posts/new')
            self.response.out.write(template.render(path, template_values))
    
    class Show(webapp.RequestHandler):
        def get(self, post_id):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write(post_id)
    
    class Edit(webapp.RequestHandler):
        def get(self, post_id):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write("edit: " + post_id)
    
    class Delete(webapp.RequestHandler):
        def get(self, post_id):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write("delete: " + post_id)

application = webapp.WSGIApplication([
                                      ('/', MainPage),
                                      ("/posts/new", Post.New),
                                      ("/posts/new.js", Post.New),
                                      ('/posts/([0-9]*)', Post.Show),
                                      ('/posts/([0-9]*)/edit', Post.Edit),
                                      ('/posts/([0-9]*)/delete', Post.Delete)
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
