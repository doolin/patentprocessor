#!/usr/bin/env python

import sys
import couchdb

attrs = ['country', 'patent', 'kind', 'date_grant', 'pat_type', \
         'date_app', 'country_app', 'patent_app', 'code_app', \
         'clm_num', 'classes', 'abstract', 'invention_title', \
         'asg_list', 'cit_list', 'rel_list', \
         'inv_list', 'law_list']

couch = couchdb.Server()
db = None
if 'patents' in couch:
    db = couch['patents']
else:
    db = couch.create('patents')

def get_metadata(patent):
    """
    Return metadata dictionary of the patent
    """
    metadata = {}
    metadata['publication_id'] = patent.patent
    metadata['application_id'] = patent.patent_app
    metadata['xml'] = patent.orig_xmlstring
    metadata['attributes'] = {}
    for attr in attrs:
        metadata['attributes'][attr] = patent.__getattribute__(attr)
    return metadata

def add_doc(metadata):
    """
    Adds metadata to couch database
    """
    doc_id, doc_rev = db.save(metadata)
    return doc_id

def query(tag, value):
    """
    Composes a javascript query to be run on the database
    """
    mapfun = """function(doc) {{
                  if(doc.{0} == "{1}")
                    emit(doc, doc.{0})
                }}""".format(tag,value)
    res = db.query(mapfun).rows
    return res[0].key['xml'] if res else None
