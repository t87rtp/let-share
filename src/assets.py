# -*- coding:utf-8 -*-

import os
import datetime
from scss import Scss

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Css(webapp.RequestHandler):
    def get(self, fname):
        scss_path = os.path.join(os.path.dirname(__file__), 'assets/scss/' + fname + '.css.scss')
        
        #リクエストされたファイルが存在しない場合404エラー
        if not os.path.exists(scss_path):
            self.response.set_status(404)
            return

        #リクエストされたファイルの最終更新日時をチェックして更新されていなければ304レスポンス
        updated_at = datetime.datetime.fromtimestamp(os.stat(scss_path).st_mtime)
        if 'If-Modified-Since' in self.request.headers:
            cached = datetime.datetime.strptime(self.request.headers['If-Modified-Since'], '%a, %d %b %Y %H:%M:%S GMT')
            current = updated_at - datetime.timedelta(seconds=1)
            if cached > current:
                self.response.set_status(304)
                return
        
        
        expires = datetime.datetime.now() + datetime.timedelta(days=365)
        self.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.response.headers['Cache-Control'] = 'private, max-age=86400'
        self.response.headers['Last-Modified'] = updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
        with open(scss_path, 'r') as f:
            data = f.read()
        scss_opts = {
                     'compress': True,
                     'debug_info': True,
                     }

        css = Scss(scss_opts=scss_opts, search_paths=[os.path.join(os.path.dirname(__file__), 'assets/scss/')])
        result = css.compile(data)
        self.response.headers['Content-Type'] = 'text/css'
        self.response.out.write(result)

application = webapp.WSGIApplication([
                                      ('/assets/css/(.*).css', Css)
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
