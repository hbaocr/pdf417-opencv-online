import os
import sys


# load current path to sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import httpServerMultiThread as httpService

# this means that if this script is executed, then  main() will be executed
if __name__ == '__main__':
    value = os.getenv("SERVER_PORT", "3000")
    port=int(value)
    print('http server run on port: ',port)
    httpService.run("0.0.0.0",port)