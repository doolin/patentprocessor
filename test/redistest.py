import sys
sys.path.append( '.' )

import redis

from patXML import XMLPatent
from patXML import uniasc
from fwork  import *
import os, datetime, re

flder = '/var/share/patentdata/patents/2010'

t1 = datetime.datetime.now()

#get a listing of all files within the directory that follow the naming pattern
files = [x for x in os.listdir(flder) if re.match(r"ipg\d{6}.xml", x, re.I)!=None]

print "Total files: %d" % (len(files))

#sys.exit()

tables = ["assignee", "citation", "class", "inventor", "patent", "patdesc", "lawyer", "sciref", "usreldoc"]
total_count = 0
total_patents = 0

r = redis.StrictRedis(host='localhost', port=6379, db=0)
#r = redis.Redis(host='localhost', port=6379, db=0)

for filenum, filename in enumerate(files):
    print " > Regular Expression: %s" % filename
    XMLs = re.findall(
            r"""
                ([<][?]xml[ ]version.*?[>]       #all XML starts with ?xml
                .*?
                [<][/]us[-]patent[-]grant[>])    #and here is the end tag
             """,
            open(flder+"/"+files[filenum]).read(), re.I + re.S + re.X)
    print "   - Total Patents: %d" % (len(XMLs))


    for i, x in enumerate(XMLs):
        r.set(i,x)
