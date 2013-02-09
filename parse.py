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
from patSQL import *
from argconfig_parse import ArgHandler
import couch_patent

xmlclasses = [AssigneeXML, CitationXML, ClassXML, InventorXML, \
              PatentXML, PatdescXML, LawyerXML, ScirefXML, UsreldocXML]

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
    if not files:
        logging.error("No files matching {0} found in {1}/{2}".format(XMLREGEX,PATENTROOT,DIRECTORIES))
        sys.exit(1)
    return files

def parse_file(filename):
    if not filename: return
    parsed_xmls = []
    size = os.stat(filename).st_size
    with open(filename,'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)) as m:
            parsed_xmls.extend(regex.findall(m))
    return parsed_xmls

def parallel_parse(filelist):
    if not filelist: return
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    parsed = pool.imap(parse_file, filelist)
    return list(itertools.chain.from_iterable(parsed))

def apply_xmlclass(us_patent_grant):
    parsed_grants = []
    for xmlclass in xmlclasses:
        try:
            parsed_grants.append(xmlclass(us_patent_grant))
        except Exception as inst:
            logging.error(type(inst))
            logging.error("  - Error: %s" % (us_patent_grant[175:200]))
    return parsed_grants

def parse_patent(grant_list):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    parsed_grants = pool.imap(apply_xmlclass, grant_list)
    parsed_grants = map(list, parsed_grants)
    return itertools.chain.from_iterable(parsed_grants)

def load_sql(patent):
    patent.insert_table()

# TODO: unittest
def build_tables(parsed_grants):
    map(load_sql, parsed_grants)

def add_to_couch_db(parsed_grants):
    for us_patent_grant in parsed_grants:
        metadata = couch_patent.get_metadata(us_patent_grant)
        couch_patent.add_doc(metadata)
        del us_patent_grant.orig_xmlstring

def commit_tables():
    assignee_table.commit();
    citation_table.commit();
    class_table.commit();
    inventor_table.commit();
    patent_table.commit();
    patdesc_table.commit();
    lawyer_table.commit();
    sciref_table.commit();
    usreldoc_table.commit();


if __name__ == '__main__':

    args = ArgHandler(sys.argv[1:])

    if args.invalid_config():
        args.get_help()

    DIRECTORIES = args.get_directory_list()
    XMLREGEX = args.get_xmlregex()
    PATENTROOT = args.get_patentroot()
    VERBOSITY = args.get_verbosity()

    logfile = "./" + 'xml-parsing.log'
    logging.basicConfig(filename=logfile, level=VERBOSITY)

    t1 = datetime.datetime.now()

    files = list_files(DIRECTORIES, PATENTROOT, XMLREGEX)
    parsed_xmls = parallel_parse(files)
    parsed_grants = parse_patent(parsed_xmls)
    build_tables(parsed_grants)
    commit_tables()
    #add_to_couch_db(parsed_grants)

    #total_patents = len(parsed_xmls)
    #total_errors = len(parsed_xmls) * len(xmlclasses) - len(parsed_grants)

    #logging.info("Parsing started at %s", str(datetime.datetime.today()))
    #logging.info("Time Elapsed: %s", datetime.datetime.now()-t1)
    #logging.info("Total Patent Files: %d" % (len(files)))
    #logging.info("Total Errors: %d", total_errors)
    #logging.info("Total Patents: %d", total_patents)
