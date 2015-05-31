#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


#allStType = find_st_names('syd_map')
#ExpectedInit = allStType.difference(WeirdStType)

#Initial Version of Expected
"""
ExpectedInit = {'Arcade',
 'Av.',
 'Ave',
 'Avenue',
 'Bouldevarde',
 'Boulevard',
 'Boulevarde',
 'Broadway',
 'Bvd',
 'Circuit',
 'Close',
 'Court',
 'Crescent',
 'Drive',
 'Esplanade',
 'Gardens',
 'Grove',
 'Highway',
 'Hwy',
 'Lane',
 'Ln',
 'Parade',
 'Pde',
 'Pkwy',
 'Place',
 'Plaza',
 'Point',
 'Promanade',
 'Rd',
 'Road',
 'Square',
 'St',
 'St.',
 'Street',
 'Street)',
 'Streets',
 'Strreet',
 'Terrace',
 'Way',
 'place',
 'road',
 'st',
 'street',
 'underpass'}
 """
 #Final Version of Expected - Manually updated.
ExpectedFin = ['Arcade',
 'Avenue',
 'Boulevard',
 'Broadway',
 'Circuit',
 'Close',
 'Court',
 'Crescent',
 'Drive',
 'Esplanade',
 'Gardens',
 'Grove',
 'Highway',
 'Lane',
 'Parade',
 'Pkwy',
 'Place',
 'Plaza',
 'Point',
 'Promanade',
 'Road',
 'Square',
 'Street',
 'Terrace',
 'Way',
 'underpass']
 
 
 #Based on ExpectedInit and ExpectedFin. Includes "Androtis", "Barney", "Berith", "Bigge", "Centenary", "Clontarf", 
 #"Corination", "Rad", "Wolli", "Wollit" from WeirdStType set in road_types.py file
mapping = {"Androtis": "Bank Street",
            "Av.": "Avenue",
            "Ave": "Avenue",
            "Barney": "Barney Street",
            "Berith": "Berith Street",
            "Bigge": "Bigge Street",
            "Bouldevarde": "Boulevard",
            "Boulevarde": "Boulevard",
            "Bvd": "Boulevard",
            "Centenary": "Centenary Road",
            "Clontarf": "Clontarf Street",
            "Corination": "Corination Street",
            "Hwy": "Highway",
            "Ln": "Lane",
            "Pde": "Parade",
            "place": "Place",
            "Rd": "Road",
            "Rad": "Road",
            "road": "Road",
            "St": "Street",
            "St.": "Street",
            "Strreet": "Street",
            "st": "Street",
            "street": "Street",
            "Wolli": "Wolli Street",
            "Wollit": "Wolli Street"}

#"Street)": "Street",
"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""

OSMFILE = "syd_map"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_type = street_type[street_type.rfind(' ')+1:]
        if street_type not in ExpectedFin:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street" and elem.attrib['k'].count(':') == 1)#changed - to ensure consistency with road_types.py

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def update_name(name, mapping):
    # YOUR CODE HERE
    for k in mapping:
        try:
            if name[name.rfind(' ')+1:].strip() == k:#changed - due to re greedy behaviour this approach works best here.
                name = re.sub(k, mapping[k], name.strip())
                break
        except:
            continue
    return name

#Use the aud_nm dictionary for making corrections at the time data is written to json file. 
def audited_names():
    aud_nm = {}
    st_types = audit(OSMFILE)
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            aud_nm[name] = better_name
    return aud_nm
