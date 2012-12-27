from parsexml import Patent
from xml.sax import make_parser, handler, parseString, saxutils

d = Patent()
parseString(open('2012_1.xml').read(), d)

