#!/usr/bin/env python

import sys
import os
import argparse
import logging

class ArgHandler(object):
    
    def __init__(self, arglist):
        self.arglist = arglist

        # setup argparse
        self.parser = argparse.ArgumentParser(description=\
                'Specify source directory/directories for xml files to be parsed')
        self.parser.add_argument('--directory','-d', type=str, nargs='+', default='.',
                help='comma separated list of directories relative to $PATENTROOT that \
                parse.py will search for .xml files')
        self.parser.add_argument('--patentroot','-p', type=str, nargs='?',
                default=os.environ['PATENTROOT'] \
                if os.environ.has_key('PATENTROOT') else '/',
                help='root directory of all patent files/directories')
        self.parser.add_argument('--xmlregex','-x', type=str, 
                nargs='?', default=r"ipg\d{6}.xml",
                help='regex used to match xml files in each directory')
        self.parser.add_argument('--verbosity', '-v', type = int,
                nargs='?', default=0,
                help='Set the level of verbosity for the computation. The higher the \
                verbosity level, the less restrictive the print policy. 0 (default) \
                = error, 1 = warning, 2 = info, 3 = debug')

        # parse arguments and assign values
        args = self.parser.parse_args(self.arglist)
        self.directories = args.directory
        self.xmlregex = args.xmlregex
        self.patentroot = args.patentroot

        # adjust verbosity levels based on specified input
        logging_levels = {0: logging.ERROR,
                          1: logging.WARNING,
                          2: logging.INFO,
                          3: logging.DEBUG}
        self.verbosity = logging_levels[args.verbosity]

    def invalid_config(self):
        # double check that variables are actually set
        # we ignore the verbosity argument when determining
        # if any variables have been set by the user
        specified = [arg for arg in self.arglist if arg.startswith('-')]
        nonverbose = [opt for opt in specified if '-v' not in opt]
        return len(nonverbose) == 0
        
    def get_directory_list(self):
        return self.directories

    def get_xmlregex(self):
        return self.xmlregex

    def get_patentroot(self):
        return self.patentroot

    def get_verbosity(self):
        return self.verbosity

    def get_help(self):
        self.parser.print_help()
        sys.exit(1)
