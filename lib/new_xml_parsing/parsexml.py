#! /usr/bin/env python

import logging
import pprint
from itertools import izip, chain
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
    res = list(self.contents[k] for k in searchdict.iterkeys())
    return res if res else ''

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

  def __classes__(self):
    res = []
    for tag in ['main-classification','further-classification']:
      tmp = self._search('classification-national', tag)
      if tmp:
        res.append(tmp[0])
    res = [[x[0][:3].replace(' ',''), x[0][3:].replace(' ','')] for x in res]
    return res

  def __asg_list__(self):
    res = self._search('assignees')
    return res if res else list(res)

  def __cit_list__(self):
    pass

  def __rel_list__(self):
    pass

  def __inv_list__(self):
    pass

  def __law_list__(self):
    pass

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
    self.classes = self.__classes__()
    self.abstract = self._search('abstract')
    self.invention_title = self._search('invention-title')
    self.asg_list = self.__asg_list__()
    self.cit_list = self.__cit_list__() 
    self.rel_list = self.__rel_list__()
    self.inv_list = self.__inv_list__()
    self.law_list = self.__law_list__()
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
    print 'asg_list',self.asg_list
    print 'cit_list',self.cit_list
    print 'rel_list',self.rel_list
    print 'inv_list',self.inv_list
    print 'law_list',self.law_list
