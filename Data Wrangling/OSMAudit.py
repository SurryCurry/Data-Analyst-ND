# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from collections import defaultdict
import re, pprint

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

def audit_street_type(street_types, street_name):
    """Helper function for audit_street_names."""
    m=street_type_re.search(street_name)
    if m:
        street_type=m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_street_names(filename):
    """Function to identify all the types of streets in the dataset.
    Any street name that is not part of the EXPECTED list is added to the
    street_types dict."""
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(filename, events=('start',)):
        for tag in elem.iter('tag'):
            if tag.attrib['k']=='addr:street':
                audit_street_type(street_types, tag.attrib['v'])
    pprint.pprint(dict(street_types))

def audit_cities(filename):
    """Creates a set of all the cities in the dataset."""
    cities = set()
    for event, elem in ET.iterparse(filename, events=('start',)):
        for tag in elem.iter('tag'):
            if tag.attrib['k']=='addr:city':
                cities.add(tag.attrib['v'])
    pprint.pprint(cities)
    
def audit_counties(filename):
    """Creates a set of all the counties in the dataset."""
    counties = set()
    for event, elem in ET.iterparse(filename, events=('start',)):
        for tag in elem.iter('tag'):
            if tag.attrib['k']=='addr:county':
                counties.add(tag.attrib['v'])
    pprint.pprint(counties)
    
def audit_state_codes(filename):
    """Creates a set of all the state codes in the dataset."""
    state_codes = set()
    for event, elem in ET.iterparse(filename, events=('start',)):
        for tag in elem.iter('tag'):
            if tag.attrib['k']=='addr:state':
                state_codes.add(tag.attrib['v'])
    pprint.pprint(state_codes)
    
def audit_country_codes(filename):
    """Creates a set of all the country codes in the dataset."""
    country_codes = set()
    for event, elem in ET.iterparse(filename, events=('start',)):
        for tag in elem.iter('tag'):
            if tag.attrib['k']=='addr:country':
                country_codes.add(tag.attrib['v'])
    pprint.pprint(country_codes)
    
def audit_postcodes(filename):
    """Creates a set of all the zip codes in the dataset."""
    postcodes = set()
    for event, elem in ET.iterparse(filename, events=('start',)):
        for tag in elem.iter('tag'):
            if tag.attrib['k']=='addr:postcode':
                postcodes.add(tag.attrib['v'])
    pprint.pprint(postcodes)