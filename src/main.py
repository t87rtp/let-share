# -*- coding:utf-8 -*-

import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from models import *
from tools import *

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

class MainPage(RequestHandlerMod):
    def get(self):
        posts = db.Query(Post).fetch(1000, 0)
        if self.response_type == "json":
            self.response.out.write(ModelEncoder().encode(posts))
        else:
            template_values = {
                               "posts": db.Query(Post).fetch(100)
                               }
            path = os.path.join(os.path.dirname(__file__), 'templates/html/index.html')
            self.response.out.write(template.render(path, template_values))

class Posts:
    class New(RequestHandlerMod):
        def get(self):
            template_values = {
                               }
            path = os.path.join(os.path.dirname(__file__), 'templates/html/editor.html')
            self.response.out.write(template.render(path, template_values))

        def post(self):
            post = Post()
            post.title = self.request.get("title")
            post.body = self.request.get("body")
            post.put()
            waitForDataPut(post)
            self.redirect("/posts/" + str(post.key().id()))
    
    class Show(RequestHandlerMod):
        def get(self, post_id):
            #参照するPostエンティティを抽出
            post = Post.get_by_id(int(post_id))
            #postが空なら404エラー
            if post == None:
                self.error(404)
                return
            
            template_values = {
                               "post": post
                               }
            path = os.path.join(os.path.dirname(__file__), 'templates/html/show.html')
            self.response.out.write(template.render(path, template_values))
    
    class Javascript(RequestHandlerMod):
        def get(self, post_id):
            #参照するPostエンティティを抽出
            post = Post.get_by_id(int(post_id))
            #postが空なら404エラー
            if post == None:
                self.error(404)
                return

            body = post.body
            if self.request.get("immediate") == "true":
                body = post.immediate()
            
            if self.request.get("minify") == "true":
                body = slimit.minify(body)

            self.response.headers['Content-Type'] = "application/javascript"
            self.response.out.write(body)
        
    class Edit(RequestHandlerMod):
        def get(self, post_id):
            #参照するPostエンティティを抽出
            post = Post.get_by_id(int(post_id))
            #postが空なら404エラー
            if post == None:
                self.error(404)
                return
            template_values = {
                               "post": post
                               }
            path = os.path.join(os.path.dirname(__file__), 'templates/html/editor.html')
            self.response.out.write(template.render(path, template_values))
        
        def post(self, post_id):
            #参照するPostエンティティを抽出
            post = Post.get_by_id(int(post_id))
            #postが空なら404エラー
            if post == None:
                self.error(404)
                return
            post.title = self.request.get("title")
            post.body = self.request.get("body")
            post.save()
            self.redirect("/posts/" + str(post.key().id()))
    
    class Delete(RequestHandlerMod):
        def get(self, post_id):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write("delete: " + post_id)

application = webapp.WSGIApplication([
                                      ('/', MainPage),
                                      ("/posts/new", Posts.New),
                                      ("/posts/new.js", Posts.New),
                                      ('/posts/([0-9]*)', Posts.Show),
                                      ('/posts/([0-9]*).js', Posts.Javascript),
                                      ('/posts/([0-9]*)/edit', Posts.Edit),
                                      ('/posts/([0-9]*)/delete', Posts.Delete)
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
