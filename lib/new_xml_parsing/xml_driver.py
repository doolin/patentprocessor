#!/usr/bin/env python

from xml.sax import handler

class XMLElement(object):
    """
    Represents XML elements from a document. These will assist
    us in representing an XML document as a Python object.
    """

    def __init__(self, name, attributes):
        self._name = name
        self._attributes = attributes
        self.children = []
        self.is_root = False

    def __iter__(self):
        yield self

    #TODO: make sure all XMLElements behave as lists during iteration
    def __len__(self):
        return 1

