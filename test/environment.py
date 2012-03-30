#!/usr/bin/env python

print "testing for imports"

import datetime, copy, csv
import math, os, random, re, sqlite3
import sys, time, types, unicodedata
from xml.dom  import minidom
import zipfile

imports = ["foo", "bar"]

try:
    import zipfile
    print "zipfile found"
except ImportError:
    print "zipfile not found"


try:
    import igraph
    print "igraph found"
except ImportError:
    print "igraph not found"

