import os
import sys


# load current path to sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import httpService

# this means that if this script is executed, then  main() will be executed
if __name__ == '__main__':
    httpService.run()