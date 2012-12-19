from xml.dom import minidom
from types import *
from exceptions import NotImplementedError
import datetime
import csv
import os
import re
import sqlite3
import copy
import unicodedata

def uniasc(x, form='NFKD', action='replace', debug=False):
    # unicode to ascii format
    if debug:
        print x
    return unicodedata.normalize(form, x).encode('ascii', action)


def ron_d(xml, itr=0, defList=[], cat="", debug=False):
    xmlcopy = []
    if itr==0:
        pass
    else:
        xmlist = copy.copy(defList)
        for x in xml.childNodes:
            if x.nodeName[0] != "#":
                if debug:
                    print x.nodeName
                if xmlist.count(cat+x.nodeName)==0 and \
                   len(re.findall("[A-Z0-9]", innerHTML(x), re.I))>0:
                    xmlist.append(cat+x.nodeName)
                xmlist.extend(ron_d(x, itr-1, cat=cat+x.nodeName+"|", debug=debug))

        xmlcopy = copy.copy(xmlist)
        for x in xmlist:
            if xmlcopy.count(x)>1:
                xmlcopy.remove(x)
        xmlcopy.sort()
    return xmlcopy 


def innerHTML(dom_element):
    #if blank return nothing as well!
    if dom_element == '':
        return ''
    else:
        rc = ""
        for node in dom_element.childNodes:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc


def XMLstruct(strList, debug=False):
    xmlstruct = []
    for i,x in enumerate(strList):
        if debug and i%(max(1, len(strList)/20))==0:
            print i
        xmlstruct = ron_d(minidom.parseString(x), 10, defList=xmlstruct)
    return xmlstruct



"""
Each of the following build_* methods takes in a [patent], which is an
XMLPatent object, and returns a list of the fields to be inserted into the sql
tables using the SQLPatent object.
"""
def build_assignee(patent):
    ack = []
    for i,y in enumerate(patent.asg_list):
        if not y[0]:
            ack.extend([[patent.patent, y[2], y[1], y[4], y[5], y[7], y[8], i]])
        else:
            ack.extend([[patent.patent, "00", "%s, %s" % (y[2], y[1]), y[4], y[5], y[6], y[7], y[8], i]])
    return ack

def build_citation(patent):
    ack = []
    for i,y in enumerate([x for x in patent.cit_list if x[1] != ""]):
        ack.extend([[patent.patent, y[3], y[5], y[4], y[1], y[2], y[0], i]])
    return ack

def build_class(patent):
    ack = []
    for i,y in enumerate(patent.classes):
        ack.extend([[patent.patent, (i==0)*1, y[0], y[1]]])
    return ack

def build_inventor(patent):
    ack = []
    for i,y in enumerate(patent.inv_list):
        ack.extend([[patent.patent, y[1], y[0], y[2], y[3], y[4], y[5], y[6], y[8], i]])
    return ack

def build_patent(patent):
    return [[patent.patent, patent.kind, patent.clm_num, patent.code_app, patent.patent_app, patent.date_grant, patent.date_grant[:4], patent.date_app, patent.date_app[:4], patent.pat_type]]

def build_patdesc(patent):
    return [[patent.patent, patent.abstract, patent.invention_title]]

def build_lawyer(patent):
    ack = []
    for i,y in enumerate(patent.law_list):
        ack.extend([[patent.patent, y[1], y[0], y[2], y[3], i]])
    return ack

def build_sciref(patent):
    ack = []
    for i,y in enumerate([y for y in patent.cit_list if y[1] == ""]):
        ack.extend([[patent.patent, y[-1], i]])
    return ack

def build_usreldoc(patent):
    ack = []
    for i,y in enumerate(patent.rel_list):
        if y[1] == 1:
            ack.extend([[patent.patent, y[0], y[1], y[3], y[2], y[4], y[5], y[6]]])
        else:
            ack.extend([[patent.patent, y[0], y[1], y[3], y[2], y[4], "", ""]])
    return ack
    
# callback structure for tblBuild
callbacks = {
    'assignee': build_assignee,
    'citation': build_citation,
    'class': build_class,
    'inventor': build_inventor,
    'patent': build_patent,
    'patdesc': build_patdesc,
    'lawyer': build_lawyer,
    'sciref': build_sciref,
    'usreldoc': build_usreldoc
    }


def uniasc(x, form='NFKD', action='replace', debug=False):
    # unicode to ascii format
    if debug:
        print x
    return unicodedata.normalize(form, x).encode('ascii', action)


def ron_d(xml, itr=0, defList=[], cat="", debug=False):
    xmlcopy = []
    if itr==0:
        pass
    else:
        xmlist = copy.copy(defList)
        for x in xml.childNodes:
            if x.nodeName[0] != "#":
                if debug:
                    print x.nodeName
                if xmlist.count(cat+x.nodeName)==0 and \
                   len(re.findall("[A-Z0-9]", innerHTML(x), re.I))>0:
                    xmlist.append(cat+x.nodeName)
                xmlist.extend(ron_d(x, itr-1, cat=cat+x.nodeName+"|", debug=debug))

        xmlcopy = copy.copy(xmlist)
        for x in xmlist:
            if xmlcopy.count(x)>1:
                xmlcopy.remove(x)
        xmlcopy.sort()
    return xmlcopy 


def innerHTML(dom_element):
    #if blank return nothing as well!
    if dom_element == '':
        return ''
    else:
        rc = ""
        for node in dom_element.childNodes:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc


def XMLstruct(strList, debug=False):
    xmlstruct = []
    for i,x in enumerate(strList):
        if debug and i%(max(1, len(strList)/20))==0:
            print i
        xmlstruct = ron_d(minidom.parseString(x), 10, defList=xmlstruct)
    return xmlstruct

class XMLPatentBase(object):
    """
    Base class for specific table-oriented patent subclasses
    """
    def __init__(self, xmlstring):
        """
        [xmlstring]: string containing xml document. Should be provided by 
        parse.py
        """
        # lowercase all tags
        self.xmlstring = re.sub(r"<[/]?[A-Za-z-]+?[ >]", lambda x: x.group().lower(), xmlstring)
        # store the minidom parsed xml doc
        self.xmldoc = minidom.parseString(self.xmlstring)
        
        # country, patent, kind, date_grant
        self.country, self.patent, self.kind, self.date_grant = self.__tagNme__(self.xmldoc, ["publication-reference", ["country", "doc-number", "kind", "date"]])
        # pat_type
        self.pat_type = self.__tagNme__(self.xmldoc, ["application-reference"], iHTML=False)[0].attributes["appl-type"].value
        # date_app, country_app, patent_app
        self.date_app, self.country_app, self.patent_app = self.__tagNme__(self.xmldoc, ["application-reference", ["date", "country", "doc-number"]])
        # code_app
        self.code_app = self.__tagNme__(self.xmldoc, ["us-application-series-code"])
        # clm_num
        self.clm_num = self.__tagNme__(self.xmldoc, ["number-of-claims"])
        # classes
        self.classes = [[x[:3].replace(' ',''), x[3:].replace(' ','')] for x in self.__tagNme__(self.xmldoc, ["classification-national", ["main-classification", "further-classification"]], idx=1, listType=True)]
        # abstract
        self.abstract = self.__allHTML__(self.xmldoc, ["abstract", "p"])
        # invention_title
        self.invention_title = self.__allHTML__(self.xmldoc, ["invention-title"])
        # asg_list
        self.asg_list = self.__asg_detail__(self.__tagNme__(self.xmldoc, ["assignees", "assignee"], iHTML=False))
        # cit_list
        self.cit_list = self.__cit_detail__(self.__tagNme__(self.xmldoc, ["references-cited", "citation"], iHTML=False))
        # rel_list
        self.rel_list = self.__rel_detail__(self.__tagNme__(self.xmldoc, ["us-related-documents"], iHTML=False))
        # inv_list
        self.inv_list = self.__tagSplit__(self.xmldoc, ["parties", "applicant"], [["addressbook", ["last-name", "first-name"]], ["addressbook", "address", ["street", "city", "state", "country", "postcode"]], [["nationality", "residence"], "country"]], blank=True)
        # law_list
        self.law_list = self.__tagSplit__(self.xmldoc, ["parties", "agents", "agent"], [["addressbook", ["last-name", "first-name", "country", "orgname"]]], blank=True)

    def build_table(self):
      raise NotImplementedError("build_table not defined for XMLPatentBase")
    
    def insert_table(self):
      raise NotImplementedError("insert_table not defined for XMLPatentBase")

    """
    These are all methods from the old XMLPatent class. I'm keeping them
    in here to assist in the carry-over of parsing the xml fields
    """
    def __allHTML__(self, xmldoc, tagList):
        """
        Replaces the html tags for everything returned by __tagName__(taglist)
        with nothing
        """
        for x in self.__tagNme__(xmldoc, tagList, iHTML=False):
            return re.sub(r"<[/]?%s( .*?)?>" % (tagList[-1]), "", x.toxml())
        return ""

    def __innerHTML__(self, dom_element):
        """
        Gets the text out of all child nodes for a certain
        dom_element
        """
        #if blank return nothing as well!
        if dom_element == '':
            return ''
        else:
            rc = ""
            for node in dom_element.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    rc = rc + node.data
            return rc

    def __tagSplit__(self, xmldoc, xmlList, tagList, baseList=[], idx=0, blank=False, iHTML=True, debug=False):
        """
        For each item in the list of xml tags returned by tagName, we treat each tag's contents
        as its own xml doc and search it for a list of xml tags. Everyything is appended together
        and returned
        """
        d_list = []
        for x in self.__tagNme__(xmldoc, tagList=xmlList, iHTML=False):
            record = copy.copy(baseList)
            for y in tagList:
                if debug:
                    print "-------------------"
                    print x.toxml()
                    print y
                record.extend(self.__tagNme__(x, tagList=y, blank=blank, iHTML=iHTML, debug=debug, idx=idx))
            d_list.append(record)
        return d_list

    def __tagNme__(self, xmldoc, tagList, idx=0, listType=False, blank=False, iHTML=True, debug=False):
        """
        takes in the xml.minidom parsed xml document [xmldoc] and a list of tags [tagList]
        [tagList] may sometimes be a list of lists?
        We iterate the taglist, searching another level deeper into the xml doc with each
        iteration. In tagList, index 0 is the first level of the xmldoc, index 1 is the list
        of all tags we look for at the level right under all the tags we found at index 0,
        and so on.
        For each item, we then iterate through all xmldocs we passed in (usually one?)
        and append the tag we wanted to an xmllist.
        We have empty strings if the tag was not found, and always return a flat list.
        **Returns:
        if the iHTML flag is set, we do the innerHTML method on the xmllist, otherwise
        we just return the xmllist.
        """
        xmldoc = [xmldoc]
        for i,x in enumerate(tagList):
            if type(x) is not ListType:
                x = [x]
            xmlnext = []
            for y in x:
                for z in xmldoc:
                    if z != '':
                        if i==0 and idx!=0:
                            if len(z.getElementsByTagName(y))>0:
                                xmlnext.append(z.getElementsByTagName(y)[idx-1])
                            else:
                                xmlnext.append('')
                        else:
                            blFlag = False
                            for za in z.getElementsByTagName(y):
                                blFlag = True
                                xmlnext.append(za)
                            if blFlag==False and blank==True:
                                xmlnext.append('')
                    else:
                        xmlnext.append('')
            xmldoc = xmlnext

        if debug:
            if len(xmldoc)==1 and iHTML:
                print self.__innerHTML__(xmldoc[0])
            elif iHTML:
                print [self.__innerHTML__(x) for x in xmldoc]
            else:
                print xmldoc

        if len(xmldoc)==1 and iHTML:
            if listType:
                return [self.__innerHTML__(xmldoc[0])]
            else:
                return self.__innerHTML__(xmldoc[0])
        elif iHTML:
            return [self.__innerHTML__(x) for x in xmldoc]
        else:
            return xmldoc

    def __asg_detail__(self, xmldoc):
        d_list = []
        for x in xmldoc:
            record = []
            if len(x.getElementsByTagName("first-name"))>0:
                record = [1]
                record.extend(self.__tagNme__(x, [["last-name", "first-name"]]))
            else:
                record = [0]
                record.extend(self.__tagNme__(x, [["orgname", "role"]]))
            record.extend(self.__tagNme__(x, ["addressbook", "address", ["street", "city", "state", "country", "postcode"]], blank=True))
            record.extend(self.__tagNme__(x, [["nationality", "residence"], "country"], blank=True))
            d_list.append(record)
        return d_list

    def __cit_detail__(self, xmldoc):
        d_list = []
        for x in xmldoc:
            #this means patcit is part of the XML
            record = [self.__tagNme__(x, ["category"])]
            if len(x.getElementsByTagName("patcit"))>0:
                record.extend(self.__tagNme__(x, ["patcit", ["country", "doc-number", "date", "kind", "name"]], blank=True))
                record.extend([""])
            elif len(x.getElementsByTagName("othercit"))>0:
                record.extend(["", "", "", "", ""])
                record.extend([self.__allHTML__(x, ["othercit"])])
                #probably should grab date information
            else:
                print x.toxml()
            d_list.append(record)
        return d_list

    def __rel_detail__(self, xmldoc, debug=False):
        d_list = []
        for x in xmldoc:
            for y in ["continuation-in-part", "continuation", "division", "reissue"]:
                if len(x.getElementsByTagName(y))>0:
                    d_list.extend(self.__tagSplit__(x, ["relation", "child-doc"], [[["doc-number", "country", "kind"]]], baseList=[y, -1], blank=True))
                    d_list.extend(self.__tagSplit__(x, ["relation", "parent-doc"], [[["doc-number", "country", "kind", "date", "parent-status"]]], baseList=[y, 1], blank=True, idx=1))
                    d_list.extend(self.__tagSplit__(x, ["relation", "parent-doc", "parent-grant-document"], [[["doc-number", "country", "kind", "date", "parent-status"]]], baseList=[y, 1], blank=True))
                    d_list.extend(self.__tagSplit__(x, ["relation", "parent-doc", "parent-pct-document"],  [[["doc-number", "country", "kind", "date", "parent-status"]]], baseList=[y, 1], blank=True))
            for y in ["related-publication", "us-provisional-application"]:
                if len(x.getElementsByTagName(y))>0:
                    d_list.extend(self.__tagSplit__(x, ["document-id"], [[["doc-number", "country", "kind"]]], baseList=[y, 0], blank=True))
            if debug:
                print "-------------------"
                for x in d_list:
                    print x
        return d_list

    def __repr__(self):
        return \
"""country = %s, patent = %s, pat_type = %s,
date_grant = %s, date_app = %s,
         abstract = %s
  invention_title = %s
len(classes, asg, cit, ret, inv, law) = %s""" % (self.country, self.patent, self.pat_type, self.date_grant, self.date_app,
       self.abstract[:50], self.invention_title[:50],
       str([len(self.classes),  len(self.asg_list), len(self.cit_list),
            len(self.rel_list), len(self.inv_list), len(self.law_list)]))


class AssigneeXML(XMLPatentBase):
    def build_table(self):
        ack = []
        for i,y in enumerate(self.asg_list):
            if not y[0]:
                ack.extend([[self.patent, y[2], y[1], y[4], y[5], y[6], y[7], y[8], i]])
            else:
                ack.extend([[self.patent, "00", "%s, %s" % (y[2], y[1]), y[4], y[5], y[6], y[7], y[8], i]])
        return ack

    def insert_table(self):
        conn = sqlite3.connect("assignee.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS assignee (
                Patent VARCHAR(8),      AsgType INTEGER,        Assignee VARCHAR(30),
                City VARCHAR(10),       State VARCHAR(2),       Country VARCHAR(2),
                Nationality VARCHAR(2), Residence VARCHAR(2),   AsgSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqAsg ON assignee (Patent, AsgSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO assignee VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",  \
            self.build_table())
        conn.commit()

class CitationXML(XMLPatentBase):
    def build_table(self):
        ack = []
        for i,y in enumerate([x for x in self.cit_list if x[1] != ""]):
            ack.extend([[self.patent, y[3], y[5], y[4], y[1], y[2], y[0], i]])
        return ack

    def insert_table(self):
        conn = sqlite3.connect("citation.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS citation (
                Patent VARCHAR(8),      Cit_Date INTEGER,       Cit_Name VARCHAR(10),
                Cit_Kind VARCHAR(1),    Cit_Country VARCHAR(2), Citation VARCHAR(8),
                Category VARCHAR(15),   CitSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqCit ON citation (Patent, CitSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO citation VALUES (?, ?, ?, ?, ?, ?, ?, ?)""" , \
            self.build_table())
        conn.commit()

class ClassXML(XMLPatentBase):
    def build_table(self):
        ack = []
        for i,y in enumerate(self.classes):
            ack.extend([[self.patent, (i==0)*1, y[0], y[1]]])
        return ack

    def insert_table(self):
        conn = sqlite3.connect("class.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS class (
                Patent VARCHAR(8),      Prim INTEGER,
                Class VARCHAR(3),       SubClass VARCHAR(3));
            CREATE UNIQUE INDEX IF NOT EXISTS uqClass ON class (Patent, Class, SubClass);
            """)
        c.executemany("""INSERT OR IGNORE INTO class VALUES (?, ?, ?, ?)""" , \
            self.build_table())
        conn.commit()

class InventorXML(XMLPatentBase):
    def build_table(self):
        ack = []
        for i,y in enumerate(self.inv_list):
            ack.extend([[self.patent, y[1], y[0], y[2], y[3], y[4], y[5], y[6], y[8], i]])
        return ack

    def insert_table(self):
        conn = sqlite3.connect("inventor.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS inventor (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                Street VARCHAR(15),     City VARCHAR(10),
                State VARCHAR(2),       Country VARCHAR(12),
                Zipcode VARCHAR(5),     Nationality VARCHAR(2), InvSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqInv ON inventor (Patent, InvSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO inventor VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" , \
            self.build_table())
        conn.commit()


class PatentXML(XMLPatentBase):
    def build_table(self):
        return [[self.patent, self.kind, self.clm_num, self.code_app, self.patent_app, self.date_grant, self.date_grant[:4], self.date_app, self.date_app[:4], self.pat_type]]

    def insert_table(self):
        conn = sqlite3.connect("patent.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS patent (
                Patent VARCHAR(8),      Kind VARCHAR(3),        Claims INTEGER,
                AppType INTEGER,        AppNum VARCHAR(8),
                GDate INTEGER,          GYear INTEGER,
                AppDate INTEGER,        AppYear INTEGER, PatType VARCHAR(15) );
            CREATE UNIQUE INDEX IF NOT EXISTS uqPat on patent (Patent);
            """)
        c.executemany("""INSERT OR IGNORE INTO patent VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" , \
            self.build_table())
        conn.commit()


class PatdescXML(XMLPatentBase):
    def build_table(self):
        return [[self.patent, self.abstract, self.invention_title]]

    def insert_table(self):
        conn = sqlite3.connect("patdesc.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS patdesc (
                Patent VARCHAR(8),
                Abstract VARCHAR(50),   Title VARCHAR(20));
            CREATE UNIQUE INDEX IF NOT EXISTS uqPatDesc ON patdesc (Patent);
            """)
        c.executemany("""INSERT OR IGNORE INTO patdesc VALUES (?, ?, ?)""" , \
            self.build_table())
        conn.commit()


class LawyerXML(XMLPatentBase):
    def build_table(self):
        ack = []
        for i,y in enumerate(self.law_list):
            ack.extend([[self.patent, y[1], y[0], y[2], y[3], i]])
        return ack

    def insert_table(self):
        conn = sqlite3.connect("lawyer.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS lawyer (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                LawCountry VARCHAR(2),  OrgName VARCHAR(20),    LawSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqLawyer ON lawyer (Patent, LawSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO lawyer VALUES (?, ?, ?, ?, ?, ?)""" , \
            self.build_table())
        conn.commit()


class ScirefXML(XMLPatentBase):
    def build_table(self):
        ack = []
        for i,y in enumerate([y for y in self.cit_list if y[1] == ""]):
            ack.extend([[self.patent, y[-1], i]])
        return ack

    def insert_table(self):
        conn = sqlite3.connect("sciref.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS sciref (
                Patent VARCHAR(8),      Descrip VARCHAR(20),    CitSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqSciref ON sciref (Patent, CitSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO sciref VALUES (?, ?, ?)""" , \
            self.build_table())
        conn.commit()


class UsreldocXML(XMLPatentBase):
    def build_table(self):
        ack = []
        for i,y in enumerate(self.rel_list):
            if y[1] == 1:
                ack.extend([[self.patent, y[0], y[1], y[3], y[2], y[4], y[5], y[6]]])
            else:
                ack.extend([[self.patent, y[0], y[1], y[3], y[2], y[4], "", ""]])
        return ack

    def insert_table(self):
        conn = sqlite3.connect("usreldoc.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS usreldoc (
                Patent VARCHAR(8),      DocType VARCHAR(10),    OrderSeq INTEGER,
                Country VARCHAR(2),     RelPatent VARCHAR(8),   Kind VARCHAR(2),
                RelDate INTEGER,        Status VARCHAR(10));
            CREATE UNIQUE INDEX IF NOT EXISTS uqUSRelDoc ON usreldoc (Patent, OrderSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO usreldoc VALUES (?, ?, ?, ?, ?, ?, ?, ?)""" , \
            self.build_table())
        conn.commit()


# old class -- to be deprecated
class XMLPatent(object):
    """
    Base class for handling parsing of xml fields
    """

    def __init__(self, xmlstring):
        """
        [xmlstring]: string containing xml document. Should be provided by 
        parse.py
        """
        # lowercase all tags
        self.xmlstring = re.sub(r"<[/]?[A-Za-z-]+?[ >]", lambda x: x.group().lower(), xmlstring)
        # store the minidom parsed xml doc
        self.xmldoc = minidom.parseString(self.xmlstring)
        
        # country, patent, kind, date_grant
        self.country, self.patent, self.kind, self.date_grant = self.__tagNme__(self.xmldoc, ["publication-reference", ["country", "doc-number", "kind", "date"]])
        # pat_type
        self.pat_type = self.__tagNme__(self.xmldoc, ["application-reference"], iHTML=False)[0].attributes["appl-type"].value
        # date_app, country_app, patent_app
        self.date_app, self.country_app, self.patent_app = self.__tagNme__(self.xmldoc, ["application-reference", ["date", "country", "doc-number"]])
        # code_app
        self.code_app = self.__tagNme__(self.xmldoc, ["us-application-series-code"])
        # clm_num
        self.clm_num = self.__tagNme__(self.xmldoc, ["number-of-claims"])
        # classes
        self.classes = [[x[:3].replace(' ',''), x[3:].replace(' ','')] for x in self.__tagNme__(self.xmldoc, ["classification-national", ["main-classification", "further-classification"]], idx=1, listType=True)]
        # abstract
        self.abstract = self.__allHTML__(self.xmldoc, ["abstract", "p"])
        # invention_title
        self.invention_title = self.__allHTML__(self.xmldoc, ["invention-title"])
        # asg_list
        self.asg_list = self.__asg_detail__(self.__tagNme__(self.xmldoc, ["assignees", "assignee"], iHTML=False))
        # cit_list
        self.cit_list = self.__cit_detail__(self.__tagNme__(self.xmldoc, ["references-cited", "citation"], iHTML=False))
        # rel_list
        self.rel_list = self.__rel_detail__(self.__tagNme__(self.xmldoc, ["us-related-documents"], iHTML=False))
        # inv_list
        self.inv_list = self.__tagSplit__(self.xmldoc, ["parties", "applicant"], [["addressbook", ["last-name", "first-name"]], ["addressbook", "address", ["street", "city", "state", "country", "postcode"]], [["nationality", "residence"], "country"]], blank=True)
        # law_list
        self.law_list = self.__tagSplit__(self.xmldoc, ["parties", "agents", "agent"], [["addressbook", ["last-name", "first-name", "country", "orgname"]]], blank=True)

        """
        Callback structure to handle the build_table specifics
        """
        self.tablecallbacks = {
            'assignee': self.build_assignee,
            'citation': self.build_citation,
            'class': self.build_class,
            'inventor': self.build_inventor,
            'patent': self.build_patent,
            'patdesc': self.build_patdesc,
            'lawyer': self.build_lawyer,
            'sciref': self.build_sciref,
            'usreldoc': self.build_usreldoc
            }

        """
        Callback structure for inserting patent into table
        """
        self.insertcallbacks = {
            'assignee': self.insert_assignee,
            'citation': self.insert_citation,
            'class': self.insert_class,
            'inventor': self.insert_inventor,
            'patent': self.insert_patent,
            'patdesc': self.insert_patdesc,
            'lawyer': self.insert_lawyer,
            'sciref': self.insert_sciref,
            'usreldoc': self.insert_usreldoc
        }


    def build_table(self, tablename):
        """
        Return list of requisite fields for inserting this patent into [tablename]
        """
        return self.tablecallbacks[tablename]()

    def build_assignee(self):
        ack = []
        for i,y in enumerate(self.asg_list):
            if not y[0]:
                ack.extend([[self.patent, y[2], y[1], y[4], y[5], y[6], y[7], y[8], i]])
            else:
                ack.extend([[self.patent, "00", "%s, %s" % (y[2], y[1]), y[4], y[5], y[6], y[7], y[8], i]])
        return ack

    def build_citation(self):
        ack = []
        for i,y in enumerate([x for x in self.cit_list if x[1] != ""]):
            ack.extend([[self.patent, y[3], y[5], y[4], y[1], y[2], y[0], i]])
        return ack

    def build_class(self):
        ack = []
        for i,y in enumerate(self.classes):
            ack.extend([[self.patent, (i==0)*1, y[0], y[1]]])
        return ack

    def build_inventor(self):
        ack = []
        for i,y in enumerate(self.inv_list):
            ack.extend([[self.patent, y[1], y[0], y[2], y[3], y[4], y[5], y[6], y[8], i]])
        return ack

    def build_patent(self):
        return [[self.patent, self.kind, self.clm_num, self.code_app, self.patent_app, self.date_grant, self.date_grant[:4], self.date_app, self.date_app[:4], self.pat_type]]

    def build_patdesc(self):
        return [[self.patent, self.abstract, self.invention_title]]

    def build_lawyer(self):
        ack = []
        for i,y in enumerate(self.law_list):
            ack.extend([[self.patent, y[1], y[0], y[2], y[3], i]])
        return ack

    def build_sciref(self):
        ack = []
        for i,y in enumerate([y for y in self.cit_list if y[1] == ""]):
            ack.extend([[self.patent, y[-1], i]])
        return ack

    def build_usreldoc(self):
        ack = []
        for i,y in enumerate(self.rel_list):
            if y[1] == 1:
                ack.extend([[self.patent, y[0], y[1], y[3], y[2], y[4], y[5], y[6]]])
            else:
                ack.extend([[self.patent, y[0], y[1], y[3], y[2], y[4], "", ""]])
        return ack

    def insert_assignee(self):
        conn = sqlite3.connect("assignee.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS assignee (
                Patent VARCHAR(8),      AsgType INTEGER,        Assignee VARCHAR(30),
                City VARCHAR(10),       State VARCHAR(2),       Country VARCHAR(2),
                Nationality VARCHAR(2), Residence VARCHAR(2),   AsgSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqAsg ON assignee (Patent, AsgSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO assignee VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",  \
            self.tablecallbacks["assignee"]())
        conn.commit()
    
    def insert_citation(self):
        conn = sqlite3.connect("citation.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS citation (
                Patent VARCHAR(8),      Cit_Date INTEGER,       Cit_Name VARCHAR(10),
                Cit_Kind VARCHAR(1),    Cit_Country VARCHAR(2), Citation VARCHAR(8),
                Category VARCHAR(15),   CitSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqCit ON citation (Patent, CitSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO citation VALUES (?, ?, ?, ?, ?, ?, ?, ?)""" , \
            self.tablecallbacks["citation"]())
        conn.commit()

    def insert_class(self):
        conn = sqlite3.connect("class.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS class (
                Patent VARCHAR(8),      Prim INTEGER,
                Class VARCHAR(3),       SubClass VARCHAR(3));
            CREATE UNIQUE INDEX IF NOT EXISTS uqClass ON class (Patent, Class, SubClass);
            """)
        c.executemany("""INSERT OR IGNORE INTO class VALUES (?, ?, ?, ?)""" , \
            self.tablecallbacks["class"]())
        conn.commit()

    def insert_inventor(self):
        conn = sqlite3.connect("inventor.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS inventor (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                Street VARCHAR(15),     City VARCHAR(10),
                State VARCHAR(2),       Country VARCHAR(12),
                Zipcode VARCHAR(5),     Nationality VARCHAR(2), InvSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqInv ON inventor (Patent, InvSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO inventor VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" , \
            self.tablecallbacks["inventor"]())
        conn.commit()

    def insert_patent(self):
        conn = sqlite3.connect("patent.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS patent (
                Patent VARCHAR(8),      Kind VARCHAR(3),        Claims INTEGER,
                AppType INTEGER,        AppNum VARCHAR(8),
                GDate INTEGER,          GYear INTEGER,
                AppDate INTEGER,        AppYear INTEGER, PatType VARCHAR(15) );
            CREATE UNIQUE INDEX IF NOT EXISTS uqPat on patent (Patent);
            """)
        c.executemany("""INSERT OR IGNORE INTO patent VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" , \
            self.tablecallbacks["patent"]())
        conn.commit()

    def insert_patdesc(self):
        conn = sqlite3.connect("patdesc.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS patdesc (
                Patent VARCHAR(8),
                Abstract VARCHAR(50),   Title VARCHAR(20));
            CREATE UNIQUE INDEX IF NOT EXISTS uqPatDesc ON patdesc (Patent);
            """)
        c.executemany("""INSERT OR IGNORE INTO patdesc VALUES (?, ?, ?)""" , \
            self.tablecallbacks["patdesc"]())
        conn.commit()


    def insert_lawyer(self):
        conn = sqlite3.connect("lawyer.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS lawyer (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                LawCountry VARCHAR(2),  OrgName VARCHAR(20),    LawSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqLawyer ON lawyer (Patent, LawSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO lawyer VALUES (?, ?, ?, ?, ?, ?)""" , \
            self.tablecallbacks["lawyer"]())
        conn.commit()


    def insert_sciref(self):
        conn = sqlite3.connect("sciref.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS sciref (
                Patent VARCHAR(8),      Descrip VARCHAR(20),    CitSeq INTEGER);
            CREATE UNIQUE INDEX IF NOT EXISTS uqSciref ON sciref (Patent, CitSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO sciref VALUES (?, ?, ?)""" , \
            self.tablecallbacks["sciref"]())
        conn.commit()


    def insert_usreldoc(self):
        conn = sqlite3.connect("usreldoc.sqlite3")
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS usreldoc (
                Patent VARCHAR(8),      DocType VARCHAR(10),    OrderSeq INTEGER,
                Country VARCHAR(2),     RelPatent VARCHAR(8),   Kind VARCHAR(2),
                RelDate INTEGER,        Status VARCHAR(10));
            CREATE UNIQUE INDEX IF NOT EXISTS uqUSRelDoc ON usreldoc (Patent, OrderSeq);
            """)
        c.executemany("""INSERT OR IGNORE INTO usreldoc VALUES (?, ?, ?, ?, ?, ?, ?, ?)""" , \
            self.tablecallbacks["usreldoc"]())
        conn.commit()


    """
    These are all methods from the old XMLPatent class. I'm keeping them
    in here to assist in the carry-over of parsing the xml fields
    """
    def __allHTML__(self, xmldoc, tagList):
        """
        Replaces the html tags for everything returned by __tagName__(taglist)
        with nothing
        """
        for x in self.__tagNme__(xmldoc, tagList, iHTML=False):
            return re.sub(r"<[/]?%s( .*?)?>" % (tagList[-1]), "", x.toxml())
        return ""

    def __innerHTML__(self, dom_element):
        """
        Gets the text out of all child nodes for a certain
        dom_element
        """
        #if blank return nothing as well!
        if dom_element == '':
            return ''
        else:
            rc = ""
            for node in dom_element.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    rc = rc + node.data
            return rc

    def __tagSplit__(self, xmldoc, xmlList, tagList, baseList=[], idx=0, blank=False, iHTML=True, debug=False):
        """
        For each item in the list of xml tags returned by tagName, we treat each tag's contents
        as its own xml doc and search it for a list of xml tags. Everyything is appended together
        and returned
        """
        d_list = []
        for x in self.__tagNme__(xmldoc, tagList=xmlList, iHTML=False):
            record = copy.copy(baseList)
            for y in tagList:
                if debug:
                    print "-------------------"
                    print x.toxml()
                    print y
                record.extend(self.__tagNme__(x, tagList=y, blank=blank, iHTML=iHTML, debug=debug, idx=idx))
            d_list.append(record)
        return d_list

    def __tagNme__(self, xmldoc, tagList, idx=0, listType=False, blank=False, iHTML=True, debug=False):
        """
        takes in the xml.minidom parsed xml document [xmldoc] and a list of tags [tagList]
        [tagList] may sometimes be a list of lists?
        We iterate the taglist, searching another level deeper into the xml doc with each
        iteration. In tagList, index 0 is the first level of the xmldoc, index 1 is the list
        of all tags we look for at the level right under all the tags we found at index 0,
        and so on.
        For each item, we then iterate through all xmldocs we passed in (usually one?)
        and append the tag we wanted to an xmllist.
        We have empty strings if the tag was not found, and always return a flat list.
        **Returns:
        if the iHTML flag is set, we do the innerHTML method on the xmllist, otherwise
        we just return the xmllist.
        """
        xmldoc = [xmldoc]
        for i,x in enumerate(tagList):
            if type(x) is not ListType:
                x = [x]
            xmlnext = []
            for y in x:
                for z in xmldoc:
                    if z != '':
                        if i==0 and idx!=0:
                            if len(z.getElementsByTagName(y))>0:
                                xmlnext.append(z.getElementsByTagName(y)[idx-1])
                            else:
                                xmlnext.append('')
                        else:
                            blFlag = False
                            for za in z.getElementsByTagName(y):
                                blFlag = True
                                xmlnext.append(za)
                            if blFlag==False and blank==True:
                                xmlnext.append('')
                    else:
                        xmlnext.append('')
            xmldoc = xmlnext

        if debug:
            if len(xmldoc)==1 and iHTML:
                print self.__innerHTML__(xmldoc[0])
            elif iHTML:
                print [self.__innerHTML__(x) for x in xmldoc]
            else:
                print xmldoc

        if len(xmldoc)==1 and iHTML:
            if listType:
                return [self.__innerHTML__(xmldoc[0])]
            else:
                return self.__innerHTML__(xmldoc[0])
        elif iHTML:
            return [self.__innerHTML__(x) for x in xmldoc]
        else:
            return xmldoc

    def __asg_detail__(self, xmldoc):
        d_list = []
        for x in xmldoc:
            record = []
            if len(x.getElementsByTagName("first-name"))>0:
                record = [1]
                record.extend(self.__tagNme__(x, [["last-name", "first-name"]]))
            else:
                record = [0]
                record.extend(self.__tagNme__(x, [["orgname", "role"]]))
            record.extend(self.__tagNme__(x, ["addressbook", "address", ["street", "city", "state", "country", "postcode"]], blank=True))
            record.extend(self.__tagNme__(x, [["nationality", "residence"], "country"], blank=True))
            d_list.append(record)
        return d_list

    def __cit_detail__(self, xmldoc):
        d_list = []
        for x in xmldoc:
            #this means patcit is part of the XML
            record = [self.__tagNme__(x, ["category"])]
            if len(x.getElementsByTagName("patcit"))>0:
                record.extend(self.__tagNme__(x, ["patcit", ["country", "doc-number", "date", "kind", "name"]], blank=True))
                record.extend([""])
            elif len(x.getElementsByTagName("othercit"))>0:
                record.extend(["", "", "", "", ""])
                record.extend([self.__allHTML__(x, ["othercit"])])
                #probably should grab date information
            else:
                print x.toxml()
            d_list.append(record)
        return d_list

    def __rel_detail__(self, xmldoc, debug=False):
        d_list = []
        for x in xmldoc:
            for y in ["continuation-in-part", "continuation", "division", "reissue"]:
                if len(x.getElementsByTagName(y))>0:
                    d_list.extend(self.__tagSplit__(x, ["relation", "child-doc"], [[["doc-number", "country", "kind"]]], baseList=[y, -1], blank=True))
                    d_list.extend(self.__tagSplit__(x, ["relation", "parent-doc"], [[["doc-number", "country", "kind", "date", "parent-status"]]], baseList=[y, 1], blank=True, idx=1))
                    d_list.extend(self.__tagSplit__(x, ["relation", "parent-doc", "parent-grant-document"], [[["doc-number", "country", "kind", "date", "parent-status"]]], baseList=[y, 1], blank=True))
                    d_list.extend(self.__tagSplit__(x, ["relation", "parent-doc", "parent-pct-document"],  [[["doc-number", "country", "kind", "date", "parent-status"]]], baseList=[y, 1], blank=True))
            for y in ["related-publication", "us-provisional-application"]:
                if len(x.getElementsByTagName(y))>0:
                    d_list.extend(self.__tagSplit__(x, ["document-id"], [[["doc-number", "country", "kind"]]], baseList=[y, 0], blank=True))
            if debug:
                print "-------------------"
                for x in d_list:
                    print x
        return d_list

    def __repr__(self):
        return \
"""country = %s, patent = %s, pat_type = %s,
date_grant = %s, date_app = %s,
         abstract = %s
  invention_title = %s
len(classes, asg, cit, ret, inv, law) = %s""" % (self.country, self.patent, self.pat_type, self.date_grant, self.date_app,
       self.abstract[:50], self.invention_title[:50],
       str([len(self.classes),  len(self.asg_list), len(self.cit_list),
            len(self.rel_list), len(self.inv_list), len(self.law_list)]))
