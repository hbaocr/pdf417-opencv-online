# https://pymotw.com/2/BaseHTTPServer/index.html#module-BaseHTTPServer
"""
HTTPServer in httpService.py is a simple subclass of SocketServer.TCPServer, and does not use multiple threads or processes to handle requests. 
To add threading or forking, create a new class using the appropriate mix-in from SocketServer.
"""
import os
import sys
import json
import tempfile
import time
from flask import Flask, jsonify, request
from flask_cors import cross_origin

from pyzxing import BarCodeReader
import pdf417Locator

reader = BarCodeReader()

# load current path to sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)


def getMiliSecond():
    millis = int(round(time.time() * 1000))
    return millis


def parseDecodeResult(results):
    result = {
        "code": "",
        "format": "NODATA"
    }
    # print(results)
    for r in results:

        # print(isinstance(r,list),type(r))
        if isinstance(r, list):
            if 'raw' in r[0]:
                result["code"] = r[0]['raw']
                result["format"] = r[0]['format']
                return result
        else:
            if 'raw' in r:
                result["code"] = r['raw']
                result["format"] = r['format']
                return result

    return result


app = Flask(__name__)


@app.route('/healthcheck')
@cross_origin()
def healthcheck():
    return jsonify(status='OK')


@app.route('/decodeImg', methods=['POST'])
@cross_origin()
def decode():
    ret = {
        "data": "",
        "status": "OK",
        "details": ""
    }
    try:
        post_data = request.get_data()
        gray = pdf417Locator.loadImgBuffer2Gray(post_data)
        pdf417_zones = pdf417Locator.locatePDF417(gray)
        l = len(pdf417_zones)
        tmpdir = ""
        with tempfile.TemporaryDirectory() as directory:
            tmpdir = directory
            for i in range(l):
                fpath = os.path.join(directory, str(i)+".jpg")
                pdf417Locator.saveBuff2Jpg(pdf417_zones[i], fpath)
                # print(fpath)
            if l > 0:
                batch_jpg = os.path.join(directory, "*.jpg")
                results = reader.decode(batch_jpg)
                code = parseDecodeResult(results)
                ret["data"] = code
    except OSError:
        ret["status"] = "FAIL"
        ret["details"] = str(OSError)

    return ret


def run(addr='0.0.0.0', port=3000):
    app.run(addr, port=port)
