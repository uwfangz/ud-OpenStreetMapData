
# coding: utf-8

# In[5]:

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint


# In[6]:

OSMFILE = "map_bellevue.osm"


# In[7]:

# UPDATE THIS VARIABLE
mapping = { "st": "Street",
            "street": "Street", #not capitalized
            "driveway": "Driveway", #not capitalized
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
            "apt": "Apartment",
            "fixme": "235th Avenue Northeast"  # all fixme streets are on the same street according to the lat and lon values
            }


# In[8]:

# Update the incorrect/overabbreviated street names:
def update(name, mapping): 
    # update the entry ending with city and state:
	if name == "144th pl ne bellevue wa":
		name = "144th pl ne"
	words = name.split()
	for w in range(len(words)):
		if words[w].lower() in mapping:  # update the street names according to the mapping variable
			words[w] = mapping[words[w].lower()]
			if words[w] == "Suite":  # For example, don't update 'Suite E' to 'Suite East'
				break
	name = " ".join(words)
	return name


# In[9]:

# write the change to a new OSM file
tree = ET.parse(OSMFILE)
root = tree.getroot()


# In[11]:

# update all street names in the data set
for elem in root.iter('tag'):
    if elem.attrib['k'] == "addr:street":
        elem.attrib['v'] = update(elem.attrib['v'], mapping)


# In[12]:

tree.write('map_bellevue_clean.osm')  # cleaned OSM file name

