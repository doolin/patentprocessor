#!/usr/bin/env python

import logging
# http://docs.python.org/howto/argparse.html
import argparse
import os
import datetime
import re
import mmap
import contextlib
import multiprocessing
import itertools

import sys
sys.path.append( '.' )
sys.path.append( './lib/' )
import shutil

from patXML import *
from fwork  import *

regex = re.compile(r"""
 ([<][?]xml[ ]version.*?[>]       #all XML starts with ?xml
.*?
[<][/]us[-]patent[-]grant[>])    #and here is the end tag
""", re.I+re.S+re.X)

def list_files(directories, patentroot, xmlregex):
    """
    Returns listing of all files within all directories relative to patentroot
    whose filenames match xmlregex
    """
    files = [patentroot+'/'+directory+'/'+fi for directory in directories for fi in \
            os.listdir(patentroot+'/'+directory) \
            if re.search(xmlregex, fi, re.I) != None]
    print files
    return files

def parse_file(filename):
    parsed_xmls = []
    size = os.stat(filename).st_size
    with open(filename,'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)) as m:
            parsed_xmls.extend(regex.findall(m))
    return parsed_xmls

def parallel_parse(filelist):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    return pool.imap_unordered(parse_file, filelist)


# setup argparse
parser = argparse.ArgumentParser(description=\
        'Specify source directory/directories for xml files to be parsed')
parser.add_argument('--directory','-d', type=str, nargs='+', default='',
        help='comma separated list of directories relative to $PATENTROOT that \
        parse.py will search for .xml files')
parser.add_argument('--patentroot','-p', type=str, nargs='?',
        default=os.environ['PATENTROOT'] \
        if os.environ.has_key('PATENTROOT') else '/',
        help='root directory of all patent files/directories')
parser.add_argument('--xmlregex','-x', type=str, 
        nargs='?', default=r"ipg\d{6}.xml",
        help='regex used to match xml files in each directory')
parser.add_argument('--verbosity', '-v', type = int,
        nargs='?', default=0,
        help='Set the level of verbosity for the computation. The higher the \
        verbosity level, the less restrictive the print policy. 0 (default) \
        = error, 1 = warning, 2 = info, 3 = debug')

# double check that variables are actually set
# we ignore the verbosity argument when determining
# if any variables have been set by the user
specified = [arg for arg in sys.argv if arg.startswith('-')]
nonverbose = [opt for opt in specified if '-v' not in opt]
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

# parse arguments and assign values
args = parser.parse_args()
DIRECTORIES = args.directory
XMLREGEX = args.xmlregex
PATENTROOT = args.patentroot
# adjust verbosity levels based on specified input
logging_levels = {0: logging.ERROR,
                  1: logging.WARNING,
                  2: logging.INFO,
                  3: logging.DEBUG}
VERBOSITY = logging_levels[args.verbosity]

logfile = "./" + 'xml-parsing.log'
logging.basicConfig(filename=logfile, level=VERBOSITY)

t1 = datetime.datetime.now()

#get a listing of all files within the directory that follow the naming pattern
files = list_files(DIRECTORIES, PATENTROOT, XMLREGEX)
logging.info("Total files: %d" % (len(files)))

# list of parsed xml strings
parsed_xmls = parallel_parse(files)
logging.info("   - Total Patents: %d" % (len(parsed_xmls._items)))

xmlclasses = [AssigneeXML, CitationXML, ClassXML, InventorXML, \
              PatentXML, PatdescXML, LawyerXML, ScirefXML, UsreldocXML]

total_count = 0
total_patents = 0

for filename in parsed_xmls:

    xmllist = []
    count = 0
    patents = 0

    for i, x in enumerate(parsed_xmls):
        for xmlclass in xmlclasses:
            try:
                xmllist.append(xmlclass(x))
                patents += 1
            except Exception as inst:
                logging.error(type(inst))
                logging.error("  - Error: %s (%d)  %s" % (filename, i, x[175:200]))
                count += 1

    logging.info("   - number of patents: %d %s ", len(xmllist), datetime.datetime.now()-t1)
    logging.info( "   - number of errors: %d", count)
    total_count += count
    total_patents += patents

    for patent in xmllist:
        patent.insert_table()

    logging.info("   - %s", datetime.datetime.now()-t1)
    logging.info("   - total errors: %d", total_count)
    logging.info("   - total patents: %d", total_patents)
