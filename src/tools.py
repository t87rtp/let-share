import json
import time
from google.appengine.ext import db

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, db.Model):
            return obj.as_dict()
        return json.JSONEncoder.default(self, obj)

def waitForDataPut(data):
    if not data.is_saved():
        time.sleep(1)
        waitForDataPut(data)
