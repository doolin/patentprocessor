#!/usr/bin/env python

from itertools import chain, izip
from collections import deque
from xml.sax import make_parser, handler, saxutils

class ChainList(list):
    """
    This is the base structure that handles the tree created by XMLElement
    and XMLHandler. Overriding __getattr__ allows us to chain queries on
    a list in order to traverse the tree.
    """

    def contents_of(self, tag, default=['']):
        res = []
        for item in self:
            res.extend( item.contents_of(tag) )
        return ChainList(res) if res else default

    def __getattr__(self, key):
        res = []
        scope = deque(self)
        while scope:
            current = scope.popleft()
            if current._name == key: res.append(current)
            else: scope.extend(current.children)
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
        self.content = []
        self.children = ChainList()
        self.is_root = False

    def __iter__(self):
        yield self

    def __nonzero__(self):
        return self.is_root or self._name is not None

    def __getitem__(self, key):
        return self.get_attribute(key)

    def __getattr__(self, key):
        res = []
        scope = deque(self.children)
        while scope:
            current = scope.popleft()
            if current._name == key: res.append(current)
            else: scope.extend(current.children)
        if res:
            self.__dict__[key] = ChainList(res)
            return ChainList(res)
        else:
            return ChainList('')

    def contents_of(self, key, default=ChainList('')):
        candidates = self.__getattr__(key)
        if candidates:
            return [x.get_content() for x in candidates]
        else:
            return default

    def get_content(self):
        if len(self.content) == 1:
            return self.content[0]
        else: return self.content

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
          self.elements[-1].content.append(saxutils.unescape(content))

class Patent(object):
    
  def __init__(self, filename):
      xh = XMLHandler()
      parser = make_parser()
      parser.setContentHandler(xh)
      parser.setFeature(handler.feature_external_ges, False)
      parser.parse(filename)
      self.xml = xh.root.us_patent_grant.us_bibliographic_data_grant
       
      self.country = self.xml.publication_reference.contents_of('country')[0]
      self.patent = self.xml.publication_reference.contents_of('doc_number')[0]
      self.kind = self.xml.publication_reference.contents_of('kind')[0]
      self.date_grant = self.xml.publication_reference.contents_of('date')[0]
      self.pat_type = self.xml.application_reference[0].get_attribute('appl-type')
      self.date_app = self.xml.application_reference.contents_of('date')[0]
      self.country_app = self.xml.application_reference.contents_of('country')[0]
      self.patent_app = self.xml.application_reference.contents_of('doc_number')[0]
      self.code_app = self.xml.contents_of('us_application_series_code')[0]
      self.clm_num = self.xml.contents_of('number_of_claims')[0]
      self.classes = self._classes()
      self.abstract = self.xml.contents_of('abstract','')
      self.invention_title = self.xml.contents_of('invention_title')[0]
      self.asg_list = self._asg_list()
      self.cit_list = self._cit_list()
      self.rel_list = self._rel_list()
      self.inv_list = self._inv_list()
      self.law_list = self._law_list()

  def has_content(self, l):
      return any(filter(lambda x: x, l))

  def _classes(self):
      main = self.xml.classification_national.contents_of('main_classification')
      further = self.xml.classification_national.contents_of('further_classification')
      it = [x[0] for x in (main,further) if self.has_content(x)]
      return [ [x[:3].replace(' ',''), x[3:].replace(' ','')] for x in it]

  def _asg_list(self):
      doc = self.xml.assignees.assignee
      data = []
      if not doc: return []
      if doc.first_name:
          data = [1]
          data.extend(doc.contents_of('last_name'))
          data.extend(doc.contents_of('first_name'))
      else:
          data = [0]
          data.extend(doc.contents_of('orgname'))
          data.extend(doc.contents_of('role'))
      for tag in ['street','city','state','country','postcode']:
          data.extend(doc.addressbook.address.contents_of(tag))
      data.extend(doc.nationality.contents_of('country'))
      data.extend(doc.residence.contents_of('country'))
      return [data]

  def _escape_html_nosub(self, string):
      lt = re.compile('<(?!/?sub>)')
      gt = re.compile('(?=.)*(?<!sub)>')
      string = string.replace('&','&amp;')
      string = re.sub(lt,"&lt;",string)
      string = re.sub(gt,"&gt;",string)
      return string

  #TODO: fix text encodings 
  def _cit_list(self):
      res = []
      cits = self.xml.references_cited.citation
      record = cits.contents_of('category')
      res.append(record)
      if cits.patcit:
          for tag in ['country','doc_number','date','kind','name']:
              res.append(cits.patcit.contents_of(tag))
          res.append( [''] * len(res[0]))
      contacts = map(list, list(izip(*res)))
      last_records = record[len(contacts):]
      if cits.othercit:
          for rec,cit in zip(last_records,cits.contents_of('othercit')):
              tmp = [rec, '', '', '', '' ,'']
              s = ''.join(cit)
              tmp.append(s)
              contacts.append(tmp)
      return contacts

  def _rel_list(self):
      res = []
      for tag in ['continuation_in_part','continuation','division','reissue']:
          if not self.xml.__getattr__(tag):
              continue
          tag = tag.replace('_','-')
          if self.xml.relation.child_doc:
              tmp = [tag, -1]
              for nested in ['doc_number','country','kind']:
                  tmp.extend(self.xml.relation.child_doc.contents_of(nested))
              res.append(tmp)
          if self.xml.relation.parent_doc:
              tmp = [tag, 1]
              for nested in ['doc_number','country','kind','date','parent_status']:
                  data = self.xml.relation.parent_doc.contents_of(nested)
                  tmp.append(data[0] if isinstance(data, list) else data)
              res.append(tmp)
          if self.xml.relation.parent_doc.parent_grant_document:
              tmp = [tag, 1]
              for nested in ['doc_number','country','kind','date','parent_status']:
                  tmp.extend(self.xml.relation.parent_grant_document.contents_of(nested))
              res.append(tmp)
          if self.xml.relation.parent_doc.parent_pct_document:
              tmp = [tag, 1]
              for nested in ['doc_number','country','kind','date','parent_status']:
                  tmp.extend(self.xml.relation.parent_pct_document.contents_of(nested))
              res.append(tmp)
          if res: break
      for tag in ['related-publication','us-provisional-application']:
          if not self.xml.__getattr__(tag):
              continue
          if self.xml.document_id:
              tmp = [tag, 0]
              for nested in ['doc_number','country','kind']:
                  tmp.extend(self.xml.document_id.contents_of(nested))
              res.append(tmp)
          if res: break
      return res

  def _inv_list(self):
      doc = self.xml.parties.applicant
      if not doc: return []
      res = []
      res.append(doc.addressbook.contents_of('last_name'))
      res.append(doc.addressbook.contents_of('first_name'))
      for tag in ['street','city','state','country','postcode']:
          res.append(doc.addressbook.address.contents_of(tag))
      res.append(doc.nationality.contents_of('country'))
      res.append(doc.residence.contents_of('country'))
      maxlen = max(map(len, res))
      res = [x*maxlen if len(x) != maxlen else x for x in res]
      return map(list, list(izip(*res)))

  def _law_list(self):
      doc = self.xml.parties.agents
      if not doc: return []
      res = []
      for agent in doc.agent:
        tmp = []
        for tag in ['last_name','first_name','country','orgname']:
            data = agent.contents_of(tag)
            tmp.extend([''.join(x) for x in data] if data else [''])
        res.append(tmp)
      return res
