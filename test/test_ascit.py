#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
Macos keycodes for common utf characters found in patents.

http://kb.iu.edu/data/anhf.html

Keystroke   Character
Option-e [letter]    acute (e.g., á)
Option-` [letter]    grave (e.g., è)
Option-i [letter]    circumflex (e.g., ô )
Option-u [letter]    umlaut or dieresis (e.g., ï )
Option-n [letter]    tilde (e.g.,  ñ )
Option-q             oe ligature ( œ )
Option-c             cedilla ( ç )
Option-Shift-/ (forward slash)  upside-down question mark ( ¿ )
Option-1 (the number 1)         upside-down exclamation point ( ¡ )
"""

import unittest
import sys
sys.path.append( '.' )
sys.path.append( '../lib/' )
from fwork import ascit

class TestAscit(unittest.TestCase):

    def setUp(self):
        self.foo = 'bar'

    def test_toupper(self):
        assert('FOO' == ascit('foo'))

    def test_remove_acute(self):
        #print 'ascit é' + ascit('é')
        assert('E' == ascit('é'))

    def test_remove_grave(self):
        assert('' == ascit('è'))

    def test_remove_circumflex(self):
        assert('' == ascit('ô'))

    def test_remove_umlaut(self):
        assert('' == ascit('ü'))

    def test_remove_tilde(self):
        assert('' == ascit('ñ'))

    def test_remove_oeligature(self):
        assert('' == ascit('œ'))

    def test_remove_cedilla(self):
        assert('' == ascit('ç'))

    def test_remove_usdq(self):
        assert('' == ascit('¿'))

    def test_int(self):
        assert('1' == ascit('1'))

    def test_float(self):
        # Default strict=True removes periods.
        result = ascit('1.0', strict=False)
        assert('1.0' == result)

    def test_remove_period(self):
        assert('10' == ascit('1.0', strict=True))


if __name__ == '__main__':
    unittest.main()
