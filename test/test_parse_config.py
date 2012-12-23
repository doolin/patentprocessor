#!/usr/bin/env python

import unittest
import os
import logging
import sys
import subprocess

# Setup test files and logs
dir = os.path.dirname(__file__)
log_file = os.path.join(dir, 'unittest/unit-test.log')

# Logging setup
logging.basicConfig(filename=log_file, level=logging.DEBUG)


class TestPatentConfig(unittest.TestCase):
    # Make sure that if os.environ['PATENTROOT'] is set, then we parse it correctly
    # if it is nonexistant/incorrect, then recover
    # if it is not set, then we default to /data/patentdata/patents

    def setUp(self):
        # make sure we can call parse.py using the os module
        # for the purpose of testing command line arguments
        self.null_out = open('/dev/null','wb')
        current_directory = os.getcwd()
        if not current_directory.endswith('test'):
            logging.error('Please run from the patentprocessor/test directory')
        # test existence of PATENTROOT; set it to reasonable default if nonexistant
        if not os.environ.has_key('PATENTROOT'):
            logging.error('Cannot find PATENTROOT environment variable. Setting ' +
                'PATENTROOT to the patentprocessor directory for the scope of this test. ' +
                'Use `export PATENTROOT=/path/to/directory` to change')
            os.environ['PATENTROOT'] = os.getcwd()
        self.assertTrue(os.access(os.environ['PATENTROOT'], os.F_OK), msg='PATENTROOT directory does not exist')
        self.assertTrue(os.access(os.environ['PATENTROOT'], os.R_OK), msg='PATENTROOT directory is not readable')
        self.assertTrue(os.environ.has_key('PATENTROOT'))
        os.chdir('..')

    def test_argparse_patentroot(self):
        # test that argparse is setting the variables correctly for patentroot
        exit_status = subprocess.call('python parse.py --patentroot %s' % \
                (os.getcwd() + '/test/unittest/fixtures'), \
                stdout=self.null_out, shell=True)
        # valid directory, but no xml files
        self.assertTrue(exit_status == 0)

        exit_status = subprocess.call('python parse.py --patentroot /asdf', \
                stdout=self.null_out, shell=True)
        # specify invalid directory, should not have any files, but still pass
        self.assertTrue(exit_status == 0)

        # test a working, valid directory
        exit_status = subprocess.call('python parse.py --patentroot %s' % \
                (os.environ['PATENTROOT']), stdout=self.null_out, shell=True)
        # this should pass
        self.assertTrue(exit_status == 0)

    def test_argparse_regex(self):
        # test that argparse is setting the regular expression correctly
        # test valid regex on unittest/fixtures folder
        exit_status = subprocess.call("python parse.py \
                --patentroot %s --xmlregex '2012_\d.xml'" % \
                (os.getcwd() + '/test/unittest/fixtures'), \
                stdout=self.null_out, shell=True)
        self.assertTrue(exit_status == 0)

    def test_argparse_directory(self):
        # test that argparse is setting the variables correctly for directories
        # parse.py should not find any .xml files, but this should still pass
        exit_status = subprocess.call('python parse.py --patentroot %s' % \
                (os.getcwd() + '/test/unittest'), stdout=self.null_out, shell=True)
        self.assertTrue(exit_status == 0)

        # parse.py should concatentate the correct directory and find xml files
        exit_status = subprocess.call("python parse.py --patentroot %s \
                --directory fixtures --xmlregex '2012_\d.xml'" % \
                (os.getcwd() + '/test/unittest'), stdout=self.null_out, shell=True)
        self.assertTrue(exit_status == 0)

        # TODO: make test for iterating through multiple directories

    def test_gets_environment_var(self):
        # sanity check for existing valid path
        logging.info("Testing getting valid env var PATENTROOT")
        self.assertTrue(os.environ.has_key('PATENTROOT'))

    def tearDown(self):
        os.chdir('test')

# TODO: Add a function which tests for existence (and maybe
# validity of PATENTROOT, and guides the user how to set it
# if its not set or invalid.
if __name__ == '__main__':

    open(log_file, 'w')
    unittest.main()
