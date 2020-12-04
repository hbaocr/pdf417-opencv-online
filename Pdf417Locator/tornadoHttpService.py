import tornado.ioloop
import tornado.web
import os
import sys
import json
import tempfile
import time
from pyzxing import BarCodeReader

class MainHandler(tornado.web.RequestHandler):
    def get(self):      
        self.write(json.dumps({'status':'OK'}).encode('utf8'))

def make_app():
    return tornado.web.Application([
        (r"/healcheck", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()