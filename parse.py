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

from patXML import *

regex = re.compile(r"""
 ([<][?]xml[ ]version.*?[>]       #all XML starts with ?xml
.*?
[<][/]us[-]patent[-]grant[>])    #and here is the end tag
""", re.I+re.S+re.X)

# TODO: put into configuration file (low priority)
xmlclasses = [AssigneeXML, CitationXML, ClassXML, InventorXML, \
              PatentXML, PatdescXML, LawyerXML, ScirefXML, UsreldocXML]


def list_files(directories, patentroot, xmlregex):
    """
    Returns listing of all files within all directories relative to patentroot
    whose filenames match xmlregex
    """
    files = [patentroot+'/'+directory+'/'+fi for directory in directories for fi in \
            os.listdir(patentroot+'/'+directory) \
            if re.search(xmlregex, fi, re.I) != None]
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
    parsed = pool.imap_unordered(parse_file, filelist)
    return list(itertools.chain.from_iterable(parsed))

def parse_patent(grant_list):
    parsed_grants = []
    for us_patent_grant in grant_list:
        for xmlclass in xmlclasses:
            try:
                parsed_grants.append(xmlclass(us_patent_grant))
            except Exception as inst:
                logging.error(type(inst))
                logging.error("  - Error: %s %s" % (us_patent_grant, us_patent_grant[175:200]))
    return parsed_grants

# TODO: unittest
def build_tables(parsed_grants):
    for us_patent_grant in parsed_grants:
        us_patent_grant.insert_table()

#TODO: pull out modular functionality into unittest-able methods
if __name__ == '__main__':

    # TODO: extract all argument parsing into fxn (in its own file)
    # setup argparse
    parser = argparse.ArgumentParser(description=\
            'Specify source directory/directories for xml files to be parsed')
    parser.add_argument('--directory','-d', type=str, nargs='+', default='.',
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
    if len(nonverbose) == 0:
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
    if not files:
        logging.error("No files matching {0} found in {1}/{2}".format(XMLREGEX,PATENTROOT,DIRECTORIES))
        sys.exit(1)

    parsed_xmls = parallel_parse(files)
    parsed_grants = parse_patent(parsed_xmls)
    build_tables(parsed_grants)

    total_patents = len(parsed_xmls)
    total_errors = len(parsed_xmls) * len(xmlclasses) - len(parsed_grants)


    logging.info("Parsing started at %s", str(datetime.datetime.today()))
    logging.info("Time Elapsed: %s", datetime.datetime.now()-t1)
    logging.info("Total Patent Files: %d" % (len(files)))
    logging.info("Total Errors: %d", total_errors)
    logging.info("Total Patents: %d", total_patents)
