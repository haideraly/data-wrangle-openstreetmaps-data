#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
import audit
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. You could also do some cleaning
before doing that, like in the previous exercise, but for this exercise you just have to
shape the structure.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""
#this returns  a dictionary which is used for cleaning street names.
adt_st = audit.audited_names()

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#I did not use the following list - only realised that it was here when I had finished my code. 
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    temp_val = ""
    #Just like case study - I have restricted to "node" and "way"
    if element.tag == "node" or element.tag == "way":
        # YOUR CODE HERE
        #element.attrib returns a dictionary in the form {"attribute": "value"}
        node["id"] = element.attrib['id']
        node["type"] = element.tag
        if element.attrib.has_key('visible'):
            node["visible"] = element.attrib['visible']
        node["created"] = {"version": element.attrib['version'], 
                           "changeset": element.attrib['changeset'], 
                           "timestamp": element.attrib['timestamp'],
                           "user": element.attrib['user'], 
                           "uid": element.attrib['uid']}
        if element.attrib.has_key('lat') and element.attrib.has_key('lon'): 
            node["pos"] = [float(element.attrib['lat']), float(element.attrib['lon'])]
        node["address"] = {}
        #Deal with the remaining attributes including address containing problematic street names.
        for tag in element.iter("tag"):
            if problemchars.match(tag.attrib['k']) is None:       
                if tag.attrib['k'].startswith('addr:') and tag.attrib['k'].count(':') == 1:
                    #For cleaning street names
                    if tag.attrib['v'] in adt_st:#if problematic use the adt_st dictionary
                        node["address"][tag.attrib['k'][tag.attrib['k'].find(':')+1:]] = adt_st[tag.attrib['v']]
                    else:
                        node["address"][tag.attrib['k'][tag.attrib['k'].find(':')+1:]] = tag.attrib['v']
                elif not tag.attrib['k'].startswith('addr:') and tag.attrib['k'].count(':') <= 1:
                    #Put changes here:
                    #newlines for "natural" or "man_made" 
                    if tag.attrib['k'][tag.attrib['k'].find(':')+1:] == "type":
                        temp_val += tag.attrib['v']
                    else:
                    #original line
                        node[tag.attrib['k'][tag.attrib['k'].find(':')+1:]] = tag.attrib['v']
        if element.tag == "way":
            node["node_refs"] = []
            for n in element.iter("nd"):
                node["node_refs"].append(n.attrib["ref"])
        #Dealing with type: natural or man_made
        if "natural" in node:
            n1 = node["natural"]
            node["natural"] = {}
            node["natural"]["type"] = n1
            node["natural"]["name"] = temp_val
        
        if "man_made" in node:
            n1 = node["man_made"]
            node["man_made"] = {}
            node["man_made"]["type"] = n1
            node["man_made"]["purpose"] = temp_val

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def wrt_file():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('syd_map', False)
    #pprint.pprint(data)