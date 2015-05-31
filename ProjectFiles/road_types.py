#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from collections import defaultdict
"""
The find_st_names() function outputs all Street Type Names in respect of "node" and "way" tags which have "addr:street" attribute

WeirdStType is manually constructed from the StType ignoring those names which are expected or problematic.


"""


StType = set()

def find_st_names(filename):
    for _, element in ET.iterparse(filename):
        if element.tag == "node" or element.tag == "way":
            for tag in element.iter("tag"):
                if tag.attrib['k'] == 'addr:street' and tag.attrib['k'].count(':') == 1:
                    StType.add(tag.attrib['v'][tag.attrib['v'].rfind(' ')+1:])
    return StType

WeirdStType = {'2150',
 'Androtis',
 'Barney',
 'Berith',
 'Bigge',
 'Centenary',
 'Clontarf',
 'Corination',
 'East',
 'Edward',
 'Illawong',
 'Jones',
 'Kingsgrove',
 'Kingsway',
 'Mall',
 'Market',
 'North',
 'Ogilve',
 'Plumpton',
 'Precinct',
 'Rad',
 'Revesby',
 'Row',
 'Shaw',
 'South',
 'Stey',
 'West',
 'Whalan',
 'Wolli',
 'Wollit',
 'Woodlands',
 'marrickville',
 'topping'}

#The following function returns a dictionary of unique id numbers in respect of each element of WeirdStType.
def find_wrd_st_names(filename):
    wrd_st_nm = defaultdict(set)
    for _, element in ET.iterparse(filename):
        if element.tag == "node" or element.tag == "way":
            for tag in element.iter("tag"):
                if tag.attrib['k'] == 'addr:street' and tag.attrib['k'].count(':') == 1:
                    k = tag.attrib['v'][tag.attrib['v'].rfind(' ')+1:]
                    if k in WeirdStType:
                        wrd_st_nm[k].add(element.attrib['id'])
    return wrd_st_nm
 