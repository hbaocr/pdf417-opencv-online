import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from pdf417Reader import BarCodeReader
reader = BarCodeReader()
results = reader.decode('../doc/test.jpg')
print(results)