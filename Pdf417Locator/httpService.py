
#https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
#https://blog.tecladocode.com/python-30-day-21-multiple-files/
#https://github.com/ChenjieXu/pyzxing
#https://yushulx.medium.com/how-to-use-python-zxing-and-python-zbar-on-windows-10-610b741c845a
#https://github.com/zxing/zxing/issues/836
# nho decode them file goc
import os
import sys
import json
import tempfile
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from pyzxing import BarCodeReader
reader = BarCodeReader()

# load current path to sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import pdf417Locator

def getMiliSecond():
    millis = int(round(time.time() * 1000))


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

class PDF417LocatorHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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

    def do_POST(self):
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
                        print(fpath)
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

def run(addr='0.0.0.0',port=3000):
    httpd = HTTPServer((addr, port), PDF417LocatorHTTPRequestHandler)
    httpd.serve_forever()

#run()

