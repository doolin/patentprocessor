#!/usr/bin/env python

print "Testing for system module i mports..."


imports = ['datetime', "copy", "csv", "math", "os", "random", "re",
           "sqlite3", "sys", "time", "types", "unicodedata", "xml",
           "zipfile", "igraph"]

def check_module(module):
    try:
        __import__(module)
        print "module %s found" % module
    except ImportError:
        print "module %s not found" % module


for module in imports:
    check_module(module)

