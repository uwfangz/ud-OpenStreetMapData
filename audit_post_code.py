import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

#osm_file = open("sample_map_xsm.osm", "r")
OSMFILE = "map_bellevue.osm"

postcode_re = re.compile(r'^[0-9]{5}(?:-[0-9]{4})?$', re.IGNORECASE)


# Check if the post code meets the regex (^[0-9]{5}(?:-[0-9]{4})?$); 
# this regex can include post code with 4 additional digits
def audit_postcode_type(wrong_types,postcode):
	m = postcode_re.search(postcode)
	if not m:
		wrong_types[postcode] += 1 #Return the zip code that do NOT match the RE and its count
		
# check if the the value of 'k' is "addr:postcode":
def is_post_code(elem):
	return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")
	
# parse the file and return the post codes that do not fit the zip code format
def audit(osmfile):
    osm_file = open(osmfile, "r")
    wrong_types = defaultdict(int)  # gather incorrect zip codes in wrong_types
    for event, elem in ET.iterparse(osm_file, events=("start",)):
    	if is_post_code(elem):
    		audit_postcode_type(wrong_types, elem.attrib['v'])
    osm_file.close()
    return wrong_types
    
# Execute audit() function and return the incorrect postcodes:
def main():
    wrong_types = audit(OSMFILE)
    pprint.pprint(dict(wrong_types))

if __name__ == '__main__':
    main()
