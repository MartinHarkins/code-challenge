import os
from os import path
import re

#Included txt files for future use as a webapp
mypath = "/home/teitoku/code-challenge/"
files = [f for f in os.listdir(mypath) if path.isfile(f) and (f.endswith(".html") or f.endswith(".txt"))]

print files
