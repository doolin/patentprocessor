#! /usr/bin/env python

import logging
import pprint
from collections import deque, defaultdict
from xml.sax import make_parser, handler, parseString, saxutils

taglist = ['country','doc-number','kind','date','application-reference','appl-type','classification-national','main-classification',
           'further-classification','abstract','invention-title','assignees','assignee','references-cited','citation','us-related-documents','parties','applicant',
           'addressbook','last-name','first-name','street','city','state','country','postcode','nationality','residence','agents','agent','orgname']

"""

By using the xml.sax.handler.ContentHandler, we can create a stack of the tags
we encounter when parsing the xml document. The information required by the
XMLPatentBase class can be described as tuples specifying the requisite nesting
of tags leading to the information that we want. E.g. (parties, applicant,
addressbook) would flexibly specify a nesting matching:

  <parties>
  <applicant>
  <addressbook> .... </addressbook>
  </applicant>
  </parties>

with an arbitrary number of tags between <parties>, <applicant> and
<addressbook>. We can map the contents of a tag to the tagstack at that point
in time. We can then search the keys of this dictionary for orderings of tags
matching the ordering in the tuple we are looking at. We have to be sure to
preserve the ordering of the tagstack keys as they are added to the dictionary
in case we need information from across multiple internal tags.

"""
class Patent(handler.ContentHandler):

  def __init__(self):
    self.tagstack = deque()
    self.contents = defaultdict(list)
    self.attributes = defaultdict(str)

  def _search(self, *terms):
    """
    Given a list [terms] of xml tags, we return the contents described
    by the nesting of tags in the order specified.
    """
    allkeys = self.contents.keys()
    searchdict = dict(zip(allkeys,allkeys))
    for term in terms:
      searchdict = dict((k,v[v.index(term):]) \
                    for k,v in searchdict.iteritems() if term in v)
    return list(self.contents[k] for k in searchdict.iterkeys())

  def startElement(self, name, attrs):
    self.tagstack.append(name)
    for k,v in attrs.items():
      self.attributes[k] = v

  def endElement(self, name):
    if self.tagstack:
      if self.tagstack[-1] == name:
        self.tagstack.pop()
  
  def characters(self, content):
    if content.strip():
      self.contents[tuple(self.tagstack)].append(content)

  def endDocument(self):
    print '--------DONE--------'
    self.country = self._search('publication-reference','country')
    self.patent = self._search('publication-reference','doc-number')
    self.kind = self._search('publication-reference','kind')
    self.date_grant = self._search('publication-reference','date')
    self.pat_type = self.attributes['appl-type']
    self.date_app = self._search('application-reference','date')
    self.country_app = self._search('application-reference','country')
    self.patent_app = self._search('application-reference','doc-number')
    self.code_app = self._search('us-application-series-code')
    self.clm_num = self._search('number-of-claims')
    self.classes = [[x[:3].replace(' ',''), x[3:].replace(' ','')] \
        for x in self._search('classification-national','main-classification')[0]]
    self.abstract = self._search('abstract')
    self.invention_title = self._search('invention-title')
    #TODO: extract the following information as according to patXML
    #self.asg_list
    #self.cit_list
    #self.rel_list
    #self.inv_list
    #self.law_list
    print 'country',self.country
    print 'patent',self.patent
    print 'kind',self.kind
    print 'date_grant',self.date_grant 
    print 'pat_type',self.pat_type
    print 'date_app',self.date_app
    print 'country_app',self.country_app 
    print 'patent_app',self.patent_app 
    print 'code_app',self.code_app 
    print 'clm_num',self.clm_num 
    print 'classes',self.classes
    print 'abstract',self.abstract 
    print 'invention_title',self.invention_title 
