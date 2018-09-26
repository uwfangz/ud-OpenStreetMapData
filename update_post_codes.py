
# coding: utf-8


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint



OSMFILE = "map_bellevue.osm"



# wrong_types = {'980452': 1, '981-2': 1, 'W Lake Sammamish Pkwy NE': 1, 'WA': 2}

# create mapping variable to correct '980452'
mapping = { "980452": "98052"}


# Update the incorrect zip code:
def update(postcode, mapping): 
    # update the entry with correct zip code:
    if postcode in mapping:
        postcode = mapping[postcode]
    else:  # update all 9-digit zip codes to 5 digits to make them consistent
        postcode = postcode.split("-")[0]
    return postcode

# write the change to a new OSM file
tree = ET.parse(OSMFILE)
root = tree.getroot()

# update the categories of 'W Lake Sammamish Pkwy NE' and 'WA'
for elem in root.iter('tag'):
    if elem.attrib['k'] == "addr:postcode":
        if elem.attrib['v'] == "W Lake Sammamish Pkwy NE":
            elem.attrib['k'] = "addr:street"
        elif elem.attrib['v'] == "WA":
            elem.attrib['k'] = "addr:state"
        else:
            elem.attrib['v'] = update(elem.attrib['v'], mapping)


tree.write('map_bellevue_clean.osm')  # write the changes to the clean OSM file

