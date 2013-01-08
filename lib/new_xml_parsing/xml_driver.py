#!/usr/bin/env python

from xml.sax import make_parser, handler

class ChainList(list):
    """
    This is the base structure that handles the tree created by XMLElement
    and XMLHandler. Overriding __getattr__ allows us to chain queries on
    a list in order to traverse the tree.
    """

    def contents_of(self, tag):
        res = []
        for item in self:
            res.extend( item.contents_of(tag) )
        return ChainList(res)

    def __getattr__(self, key):
        res = []
        for item in self:
            res.extend( filter(lambda x: x._name == key, item.children))
        return ChainList(res)

class XMLElement(object):
    """
    Represents XML elements from a document. These will assist
    us in representing an XML document as a Python object.
    Heavily inspired from: https://github.com/stchris/untangle/blob/master/untangle.py
    """

    def __init__(self, name, attributes):
        self._name = name
        self._attributes = attributes
        self.content = ''
        self.children = ChainList()
        self.is_root = False

    def __iter__(self):
        yield self

    def __nonzero__(self):
        return self.is_root or self._name is not None

    def __getitem__(self, key):
        return self.get_attribute(key)

    def __getattr__(self, key):
        candidates = filter(lambda x: x._name == key, self.children)
        if candidates:
            self.__dict__[key] = ChainList(candidates)
            return ChainList(candidates)
        else:
            raise KeyError("No such child: {0}".format(key))

    def contents_of(self, key):
        candidates = filter(lambda x: x._name == key, self.children)
        if candidates:
            return [x.content for x in candidates]
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
    
class XMLHandler(handler.ContentHandler):
    """
    SAX Handler to create the Python object while parsing
    """

    def __init__(self):
        self.root = XMLElement(None, None)
        self.root.is_root = True
        self.elements = ChainList()

    def startElement(self, name, attributes):
        name = name.replace('-','_').replace('.','_').replace(':','_')
        xmlelem = XMLElement(name, dict(attributes.items()))
        if self.elements:
            self.elements[-1].add_child(xmlelem)
        else:
            self.root.add_child(xmlelem)
        self.elements.append(xmlelem)

    def endElement(self, name):
        if self.elements:
            self.elements.pop()

    def characters(self, content):
        if content.strip():
          self.elements[-1].content = content

class Patent(object):
    
  def __init__(self, filename):
       xh = XMLHandler()
       parser = make_parser()
       parser.setContentHandler(xh)
       parser.setFeature(handler.feature_external_ges, False)
       parser.parse(filename)
       self.xml = xh.root.us_patent_grant.us_bibliographic_data_grant
        
       self.country = self.xml.publication_reference
