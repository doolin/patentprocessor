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

  def has_data(self, l):
    return filter(lambda x: x, l)

  def __classes__(self):
    res = []
    for tag in ['main-classification','further-classification']:
      tmp = self._search('classification-national', tag)
      if tmp:
        res.append(tmp[0])
    res = [[x[0][:3].replace(' ',''), x[0][3:].replace(' ','')] for x in res]
    return res

  def __asg_list__(self):
    toadd = []
    if self._search('assignees','first-name'):
      toadd = [1]
      data = self._search('assignees','last-name')
      toadd.extend(data[0] if data else [])
      data = self._search('assignees','first-name')
      toadd.extend(data[0] if data else [])
    else:
      toadd = [0]
      data = self._search('assignees','orgname')
      toadd.extend(data[0] if data else [])
      data = self._search('assignees','role')
      toadd.extend(data[0] if data else [])
    if len(toadd) == 1:
      return []
    tag = 'addressbook' if self._search('assignees','addressbook') else 'address'
    for inner in ['street','city','state','country','postcode']:
      data = self._search('assignees',tag,inner)
      toadd.extend(data[0] if data else [''])
    for tag in ['nationality','residence']:
      data = self._search('assignees',tag,'country')
      toadd.extend(data[0] if data else [''])
    return [toadd]

  def __cit_list__(self):
    basetag = 'references-cited' if self._search('references-cited') else 'citation'
    toadd = self._search(basetag,'category')
    if self._search(basetag,'patcit'):
      toadd.extend(self._search(basetag,'patcit','country'))
      toadd.extend(self._search(basetag,'patcit','doc-number'))
      toadd.extend(self._search(basetag,'patcit','date'))
      toadd.extend(self._search(basetag,'patcit','kind'))
      toadd.extend(self._search(basetag,'patcit','name'))
      toadd.append(['']*len(self._search(basetag,'patcit','name')[0]))
    elif self._search(basetag, 'othercit'):
      toadd.extend(['','','','',''])
      toadd.extend(self._search(basetag,'othercit'))
    return map(list,list(izip(*toadd)))

  def __rel_list__(self):
    d_list = []
    for tag in ['continuation-in-part','continuation','division','reissue']:
      if self._search('us-related-documents',tag):
        childtmp = []
        parenttmp = []
        parenttmpsecondary = []
        for nested in ['doc-number','country','kind']:
          data = self._search('us-related-documents',tag,'relation','child-doc',nested)
          childtmp.extend(data[0] if data else [''])
        for nested in ['doc-number','country','kind','date','parent-status']:
          data = self._search('us-related-documents',tag,'relation','parent-doc',nested)
          parenttmp.extend(data[0] if data else [''])
        for nested in ['doc-number','country','kind','date','parent-status']:
          data = self._search('us-related-documents',tag,'relation','parent-doc','parent-grant-document',nested)
          if data:
            parenttmpsecondary.extend(data[0])
          else:
            data = self._search('us-related-documents',tag,'relation','parent-doc','parent-pct-document',nested)
            parenttmpsecondary.extend(data[0] if data else [''])
        if self.has_data(childtmp):
          d_list.append([tag, -1] + childtmp)
        if self.has_data(parenttmp):
          d_list.append([tag, 1] + parenttmp)
        if self.has_data(parenttmpsecondary):
          d_list.append([tag, 1] + parenttmpsecondary)
    for tag in ['related-publication', 'us-provisional-application']:
      if self._search('us-related-documents', tag):
        for nested in ['doc-number','country','kind']:
          pass
    return d_list

  def __inv_list__(self):
    toadd = []
    for nested in ['last-name', 'first-name']:
      data = self._search('parties','applicant', 'addressbook', nested)
      toadd.append(data[0] if data else [''])
    for nested in ['street','city','state','country','postcode']:
      data = self._search('parties','applicant', 'addressbook', nested)
      toadd.append(data[0] if data else [''])
      data = self._search('parties','applicant', 'address', nested)
      toadd.append(data[0] if data else [''])
    for nested in ['nationality','residence']:
      data = self._search('parties','applicant',nested,'country')
      toadd.append(data[0] if data else [''])
    return map(list,list(izip(*toadd)))

  def __law_list__(self):
    toadd = []
    for tag in ['last-name','first-name','country','orgname']:
      data = self._search('agents','agent','addressbook',tag)
      toadd.append([''.join(data[0])] if data else [''])
    return map(list,list(izip(*toadd)))

  def endDocument(self):
    self.country = self._search('publication-reference','country')[0][0]
    self.patent = self._search('publication-reference','doc-number')[0][0]
    self.kind = self._search('publication-reference','kind')[0][0]
    self.date_grant = self._search('publication-reference','date')[0][0]
    self.pat_type = self.attributes['appl-type']
    self.date_app = self._search('application-reference','date')[0][0]
    self.country_app = self._search('application-reference','country')[0][0]
    self.patent_app = self._search('application-reference','doc-number')[0][0]
    self.code_app = self._search('us-application-series-code')[0][0]
    self.clm_num = self._search('number-of-claims')[0][0]
    self.classes = self.__classes__()
    self.abstract = self._search('abstract')
    self.invention_title = self._search('invention-title')[0][0]
    self.asg_list = self.__asg_list__()
    self.cit_list = self.__cit_list__() 
    self.rel_list = self.__rel_list__()
    self.inv_list = self.__inv_list__()
    self.law_list = self.__law_list__()
