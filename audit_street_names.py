
# coding: utf-8

# In[1]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


# In[10]:

OSMFILE = "map_bellevue.osm"


# In[11]:

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


# In[12]:

# Expected words at the end of the street names
expected = ["Alley", "Street", "Avenue", "Boulevard", "Drive", "Driveway", "Court", "Place", "Plaza", "Square", "Lane", "Road", 
            "Point", "Trail", "Parkway", "Commons", "Terrace", "Vista", "Circle", "Way", "East", "West", "North", "South", "Northeast", "Northwest", "Southeast", "Southwest"]


# In[5]:

# UPDATE THIS VARIABLE
mapping = { "st": "Street",
            "street": "Street", # not capitalized
            "driveway": "Driveway", # not capitalized
            "northest": "Northeast",  #misspelling
            "ave": "Avenue",
            "blvd": "Boulevard",
            "blvd.": "Boulevard",
            "ct": "Court",
            "d": "Drive",
            "dr.": "Drive",
            "e": "East",
            "e,": "East",
            "ln": "Lane",
            "n": "North",
            "n.": "North",
            "n.e.": "Northeast",
            "ne": "Northeast",
            "nw": "Northwest",
            "rd": "Road",
            "pl": "Place",
            "s": "South",
            "s.": "South",
            "se": "Southeast",
            "s.e.": "Southeast",
            "wy": "Way",
            "ste": "Suite",
            "apt": "Apartment"
            }


# In[13]:

# audit street type: if it's not in expected, input the entry to street_types set.
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


# In[14]:

# check if the tag is a street
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


# In[15]:

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


# In[16]:

# Execute audit() function and see if there's any street names that are abbreviated:
def main():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

if __name__ == '__main__':
    main()

