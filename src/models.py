# -*- coding:utf-8 -*-
from google.appengine.ext import db

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
    
    def promptly(self):
        return "(function(){" + self.body + "})()"
    
    def as_dict(self):
        result = super(Post, self).as_dict()
        result["promptly"] = self.promptly()
        return result
    