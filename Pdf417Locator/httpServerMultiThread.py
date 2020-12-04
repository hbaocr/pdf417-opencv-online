#https://pymotw.com/2/BaseHTTPServer/index.html#module-BaseHTTPServer
"""
HTTPServer in httpService.py is a simple subclass of SocketServer.TCPServer, and does not use multiple threads or processes to handle requests. 
To add threading or forking, create a new class using the appropriate mix-in from SocketServer.
"""
import os
import sys
import json
import tempfile
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
from pyzxing import BarCodeReader
reader = BarCodeReader()

# load current path to sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import pdf417Locator

def getMiliSecond():
    millis = int(round(time.time() * 1000))
    return millis

def parseDecodeResult(results):
    result ={
        "code":"",
        "format":"NODATA"
    }
    #print(results)
    for r in results:
    
        #print(isinstance(r,list),type(r))
        if isinstance(r,list):
            if 'raw' in r[0]:
                result["code"] =r[0]['raw']
                result["format"] =r[0]['format']
                return result
        else:
            if 'raw' in r:
                result["code"] =r['raw']
                result["format"] =r['format']
                return result

    return result

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        message =  threading.currentThread().getName()
        print('Handle Req on thread',message)

        if self.path == '/healthcheck':
            self.send_response(200)
            #self.send_header("Set-Cookie", "foo=bar")
            self.end_headers()
            self.wfile.write(json.dumps({'status':'OK'}).encode('utf8'))
        else:
            self.send_response(200)
            #self.send_header("Set-Cookie", "foo=bar")
            self.end_headers()
            self.wfile.write(json.dumps({'status':'FAIL','detail':'URL not supported'}).encode('utf8'))
       
        return

    def do_POST(self):
        message =  threading.currentThread().getName()
        print('================> Start Decode PDF417 on thread',message)

        start = getMiliSecond()
        if self.path == '/decodeImg':
            ret={
                "data":"",
                "status":"OK",
                "details":""
            }

            try:
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                post_data = self.rfile.read(content_length) # <--- Gets the data itself

                gray=pdf417Locator.loadImgBuffer2Gray(post_data)
                pdf417_zones=pdf417Locator.locatePDF417(gray)
                l=len(pdf417_zones)
                tmpdir=""
                with tempfile.TemporaryDirectory() as directory:
                    tmpdir=directory
                    for i in range(l):
                        fpath=os.path.join(directory,str(i)+".jpg")
                        pdf417Locator.saveBuff2Jpg(pdf417_zones[i],fpath)
                        #print(fpath)
                    if l>0:
                        batch_jpg=os.path.join(directory,"*.jpg")
                        results = reader.decode(batch_jpg)
                        code=parseDecodeResult(results)
                        ret["data"]=code
            except OSError:
                    ret["status"]="FAIL"
                    ret["details"]=str(OSError)

            #else:
            #    print("OK")
        

            self.send_response(200)
            #self.send_header("Set-Cookie", "foo=bar")
            self.end_headers()
            self.wfile.write(json.dumps(ret).encode('utf8'))

        else:
            self.send_response(200)
            #self.send_header("Set-Cookie", "foo=bar")
            self.end_headers()
            self.wfile.write(json.dumps({'status':'FAIL','detail':'URL not supported'}).encode('utf8'))

        period = getMiliSecond()-start
        print('Finish Decode PDF417 on thread',message," in ",period,"ms")

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def run(addr='0.0.0.0',port=3000):
    server = ThreadedHTTPServer((addr, port), Handler)
    server.serve_forever()