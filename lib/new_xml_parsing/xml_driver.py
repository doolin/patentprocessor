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

    def __getitem__(self, key):
        return self.get_attribute(key)

    def __getattr__(self, key):
        candidates = filter(lambda x: x._name == key, self.children)
        if candidates:
            self.__dict__[key] = candidates
            return candidates
        else:
            raise KeyError("No such child: {0}".format(key))

    def add_child(self, child):
        self.children.append(child)

    def get_attribute(self, key):
        return self._attributes.get(key, None)

    def get_xmlelements(self, name):
        return filter(lambda x: x._name == name, self.children) \
               if name else \
               self.children
    
        
        

