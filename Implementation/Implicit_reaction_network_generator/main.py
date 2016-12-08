import sys
from Network import *

inputFile = sys.argv[-1]

myNet = Network()
myNet.createNetwork(inputFile)

print myNet