# -*- coding:utf-8 -*-
import os
import slimit

from google.appengine.ext import db
from google.appengine.ext.webapp import template

class ModelMod(db.Model):
    def as_dict(self):
        result = {}
        for key in self.properties().keys():
            result[key] = self.__getattribute__(key)
        result["id"] = self.key().id()
        return result

class Post(ModelMod):
    title = db.StringProperty(multiline=False)
    body = db.TextProperty()
    
    def immediate(self):
        return "(function(){" + self.body + "})()"
    
    def bookmarklet(self):
        return "javascript:" + slimit.minify(self.immediate())
    
    def live_bookmarklet(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/other/live_bookmarklet.js')
        template_values = {
                           "post_id": self.key().id(),
                           "host": "http://" + os.environ.get("HTTP_HOST", "")
                           }
        return template.render(path, template_values)

    def as_dict(self):
        result = super(Post, self).as_dict()
        result["immediate"] = self.immediate()
        return result
    