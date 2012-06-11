import unittest
import sys
import imp
import os
import datetime
import re
import logging

dir = os.path.dirname(__file__)
folder = os.path.join(dir, 'unittest/')
log_file = os.path.join(dir, 'unittest/log/unit-test-log.log')
xml_files = [x for x in os.listdir(folder)
             if re.match(r".*?patent.*?xml", x) != None]

# Logging setup
logging.basicConfig(filename=log_file, level=logging.DEBUG)

class testSQLPatent(unittest.TestCase):

    def setUp(self):
        # Basic sanity check



if __name__ == '__main__':
    unittest.main()
