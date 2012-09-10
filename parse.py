#!/usr/bin/env python

import logging
# http://docs.python.org/howto/argparse.html
import argparse
import os
import datetime
import re

import sys
sys.path.append( '.' )
sys.path.append( './lib/' )
import shutil

from patXML import SQLPatent
from patXML import XMLPatent
from patXML import uniasc
from fwork  import *

# setup argparse
parser = argparse.ArgumentParser(description=\
        'Specify source directory/directories for xml files to be parsed')
parser.add_argument('--directory','-d', type=str, nargs='+', default='',\
        help='comma separated list of directories relative to $PATENTROOT that \
        parse.py will search for .xml files')
parser.add_argument('--patentroot','-p', type=str, nargs='?',\
        default=os.environ['PATENTROOT'] \
        if os.environ.has_key('PATENTROOT') else '/',\
        help='root directory of all patent files/directories')
parser.add_argument('--xmlregex','-x', type=str, \
        nargs='?', default=r"ipg\d{6}.xml",\
        help='regex used to match xml files in each directory')

# parse arguments and assign values
args = parser.parse_args()
DIRECTORIES = args.directory
XMLREGEX = args.xmlregex
PATENTROOT = args.patentroot

logfile = "./" + 'xml-parsing.log'
logging.basicConfig(filename=logfile, level=logging.DEBUG)

t1 = datetime.datetime.now()

#get a listing of all files within the directory that follow the naming pattern
files = [directory+'/'+fi for directory in DIRECTORIES for fi in \
        os.listdir(PATENTROOT+'/'+directory) \
        if re.match(XMLREGEX, fi, re.I) != None]
print "Total files: %d" % (len(files))
logging.info("Total files: %d" % (len(files)))

tables = ["assignee", "citation", "class", "inventor", "patent",\
        "patdesc", "lawyer", "sciref", "usreldoc"]
total_count = 0
total_patents = 0
for filenum, filename in enumerate(files):
    print " > Regular Expression: %s" % filename
    XMLs = re.findall(
            r"""
                ([<][?]xml[ ]version.*?[>]       #all XML starts with ?xml
                .*?
                [<][/]us[-]patent[-]grant[>])    #and here is the end tag
             """,
            open(PATENTROOT+"/"+files[filenum]).read(), re.I + re.S + re.X)
    print "   - Total Patents: %d" % (len(XMLs))
    logging.info("   - Total Patents: %d" % (len(XMLs)))


    xmllist = []
    count = 0
    patents = 0

    for i, x in enumerate(XMLs):
        try:
            xmllist.append(XMLPatent(x))
            patents += 1
        except Exception as inst:
            #print type(inst)
            logging.error(type(inst))
            print "  - Error: %s (%d)  %s" % (filename, i, x[175:200])
            logging.error("  - Error: %s (%d)  %s" % (filename, i, x[175:200]))
            count += 1
        #print xmllist

    print "   - number of patents:", len(xmllist), datetime.datetime.now()-t1
    logging.info("   - number of patents: %d %s ", len(xmllist), datetime.datetime.now()-t1)
    print "   - number of errors: ", count
    logging.info( "   - number of errors: %d", count)
    total_count += count
    total_patents += patents

    for table in tables:
        # Cut the chaining here to better parameterize the call, allowing
        # the databases to be built in place
        # (/var/share/patentdata/patents/<year>)
        # outdb = PATENTROOT + "/" + table
        q = SQLPatent().tblBuild(xmllist, tbl=table)
        SQLPatent().dbBuild(q, tbl=table, week=filename)
        #SQLPatent().dbBuild(q=SQLPatent().tblBuild(xmllist, tbl=table), tbl=table, week=filename)

    print "   -", datetime.datetime.now()-t1
    logging.info("   - %s", datetime.datetime.now()-t1)
    logging.info("   - total errors: %d", total_count)
    logging.info("   - total patents: %d", total_patents)

for table in tables:
    SQLPatent().dbFinal(tbl=table)

#for table in tables:
#    filename = table + ".sqlite3"
#    shutil.move(filename,PATENTROOT)

