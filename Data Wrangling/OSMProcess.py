# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from collections import defaultdict
import re, pprint

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

def count_tags(filename):
    """Creates a counter for the types of tags in a ElementTree."""
    tags=defaultdict(int)
    tree=ET.parse(filename)
    root=tree.getroot()
    for r in root.iter():
        tags[r.tag]+=1
    return dict(tags)

def key_type(element, keys):
    """Helper function for process_key_types."""
    if element.tag == "tag":
        k=element.attrib['k']
        if re.search(lower, k):
            keys['lower']+=1
        elif re.search(lower_colon, k):
            keys['lower_colon']+=1
        elif re.search(problemchars, k):
            keys['problemchars']+=1
        else:
            keys['other']+=1
    return keys

def process_key_types(filename):
    """Creates a dict based on regexes to search for particulary key values."""
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

def get_user(element):
    """Helper function for process_users."""
    if 'uid' in element.attrib:
        return element.attrib['uid']
    else:
        pass

def process_users(filename):
    """Creates a set to identify all the users
    who have contributed to this dataset."""
    users = set()
    for _, element in ET.iterparse(filename):
        u=get_user(element)
        if u:
            users.add(u)
    return users

def get_address_types(filename):
    """Creates a set of the different 'addr' keys in the dataset."""
    addrs=set()
    tree=ET.parse(filename)
    root=tree.getroot()
    for child in root:
        for c in child:
            if 'k' in c.attrib:
                if 'addr:' in c.attrib['k']:
                    addrs.add(c.attrib['k'])
    pprint.pprint(addrs)